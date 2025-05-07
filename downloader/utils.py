import os
import uuid
import tempfile
import shutil
import yt_dlp
from django.conf import settings

def download_media(url, format_type, video_resolution='', audio_quality='',
                  custom_format_code='', progress_callback=None):
    """
    Hàm download media từ URL với định dạng và độ phân giải được chỉ định
    Trả về thông tin về file đã tải xuống hoặc lỗi

    Args:
        url: URL video cần tải
        format_type: Định dạng đầu ra (mp3, mp4, mov, webm, etc.)
        video_resolution: Độ phân giải video (2160, 1080, 720, etc.)
        audio_quality: Chất lượng âm thanh (320, 256, 192, etc.)
        custom_format_code: Mã định dạng tùy chỉnh cho người dùng nâng cao
        progress_callback: Hàm báo cáo tiến trình tải xuống
    """
    # Tạo thư mục media nếu chưa tồn tại
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    # Tạo thư mục theo định dạng
    media_folder = 'audio' if format_type in ['mp3', 'm4a', 'opus', 'flac'] else 'video'
    media_path = os.path.join(settings.MEDIA_ROOT, media_folder)
    os.makedirs(media_path, exist_ok=True)

    # Tạo tên file duy nhất
    unique_id = str(uuid.uuid4())

    # Tạo thư mục tạm để tải xuống trước
    temp_dir = tempfile.mkdtemp()

    # Define progress hook
    def progress_hook(d):
        if d['status'] == 'downloading':
            # Calculate download percentage
            if 'total_bytes' in d and d['total_bytes'] > 0:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate'] > 0:
                percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            else:
                # If we can't determine the size, just report the downloaded size
                percent = d['downloaded_bytes'] / 1024  # KB downloaded

            # Report progress if callback is provided
            if progress_callback:
                progress_callback(round(percent, 2))

        elif d['status'] == 'finished':
            if progress_callback:
                # Report 99% - last 1% is for post-processing
                progress_callback(99)

    options = {
        'outtmpl': os.path.join(temp_dir, f'{unique_id}.%(ext)s'),
        'quiet': False,
        'verbose': True,
        'ignoreerrors': True,
        'no_warnings': False,
        'geo_bypass': True,
        'progress_hooks': [progress_hook],
        'writesubtitles': False,
        'writethumbnail': True,
    }

    # Xử lý tùy chọn định dạng
    if custom_format_code:
        # Nếu người dùng cung cấp mã tùy chỉnh, sử dụng nó
        options['format'] = custom_format_code
        file_extension = format_type  # Giả định rằng định dạng đầu ra phù hợp với lựa chọn
    elif format_type in ['mp3', 'm4a', 'opus', 'flac']:
        # Xử lý các định dạng âm thanh
        audio_format = {
            'mp3': 'mp3',
            'm4a': 'm4a',
            'opus': 'opus',
            'flac': 'flac'
        }.get(format_type, 'mp3')

        # Thiết lập chất lượng âm thanh
        quality = audio_quality if audio_quality else '192'

        options['format'] = 'bestaudio'
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': quality,
        }]
        file_extension = audio_format
        content_type = {
            'mp3': 'audio/mpeg',
            'm4a': 'audio/mp4',
            'opus': 'audio/opus',
            'flac': 'audio/flac'
        }.get(format_type, 'audio/mpeg')
    else:
        # Xử lý các định dạng video
        video_format = format_type

        # Thiết lập format string dựa trên độ phân giải yêu cầu
        if video_resolution:
            format_string = f'bestvideo[height<={video_resolution}][ext={video_format}]+bestaudio/best[height<={video_resolution}][ext={video_format}]'
        else:
            format_string = f'bestvideo[ext={video_format}]+bestaudio/best[ext={video_format}]/best'

        options['format'] = format_string

        # Nếu định dạng đầu ra khác với định dạng được chọn, cần chuyển đổi
        if format_type == 'mov':
            options['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mov',
            }]
        elif format_type == 'mkv':
            options['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mkv',
            }]

        file_extension = format_type
        content_type = {
            'mp4': 'video/mp4',
            'webm': 'video/webm',
            'mov': 'video/quicktime',
            'mkv': 'video/x-matroska'
        }.get(format_type, 'video/mp4')

    try:
        # Download video/audio
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                shutil.rmtree(temp_dir)  # Xóa thư mục tạm
                return {'success': False, 'error': 'Không thể tải video. Vui lòng thử URL hoặc định dạng khác.'}

            title = info.get('title', 'Unknown Title')
            formats = info.get('formats', [])

            # Lấy thông tin về định dạng đã chọn
            selected_format = None
            for fmt in formats:
                if fmt.get('format_id') == info.get('format_id'):
                    selected_format = fmt
                    break

            # Lấy thông tin độ phân giải và mã định dạng
            resolution = ''
            format_code = info.get('format_id', '')
            filesize = ''

            if selected_format:
                height = selected_format.get('height')
                width = selected_format.get('width')
                if height and width:
                    resolution = f"{width}x{height}"
                elif height:
                    resolution = f"{height}p"

                filesize_bytes = selected_format.get('filesize') or info.get('filesize')
                if filesize_bytes:
                    filesize = format_filesize(filesize_bytes)

        # Tìm file đã tải trong thư mục tạm
        downloaded_file = None
        for file in os.listdir(temp_dir):
            if file.startswith(unique_id):
                downloaded_file = os.path.join(temp_dir, file)
                file_extension = file.split('.')[-1]
                break

        if not downloaded_file or not os.path.exists(downloaded_file):
            shutil.rmtree(temp_dir)  # Xóa thư mục tạm
            return {'success': False, 'error': 'Tập tin tải xuống không tồn tại.'}

        # Tạo tên file an toàn
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        safe_filename = f"{safe_title}_{unique_id}.{file_extension}"

        # Tạo đường dẫn file cho DB (đường dẫn tương đối so với MEDIA_ROOT)
        relative_path = f"{media_folder}/{safe_filename}"

        # Di chuyển file từ thư mục tạm sang thư mục media
        media_file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        shutil.copy2(downloaded_file, media_file_path)

        # Report 100% progress
        if progress_callback:
            progress_callback(100)

        # Xóa thư mục tạm sau khi đã di chuyển file
        shutil.rmtree(temp_dir)

        return {
            'success': True,
            'title': title,
            'file_path': relative_path,
            'content_type': content_type,
            'format': format_type,
            'resolution': resolution,
            'format_code': format_code,
            'filesize': filesize
        }

    except Exception as e:
        # Xóa thư mục tạm nếu có lỗi
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return {'success': False, 'error': str(e)}


def get_available_formats(url):
    """
    Lấy danh sách các định dạng có sẵn từ URL
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'listformats': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return {'success': False, 'error': 'Không thể lấy thông tin video'}

            formats = []
            for format in info.get('formats', []):
                format_note = format.get('format_note', '')
                ext = format.get('ext', '')
                format_id = format.get('format_id', '')
                filesize = format.get('filesize')
                tbr = format.get('tbr')  # total bit rate
                vcodec = format.get('vcodec', 'none')
                acodec = format.get('acodec', 'none')

                # Bỏ qua các mục không quan trọng
                if vcodec == 'none' and acodec == 'none':
                    continue

                is_video = vcodec != 'none'
                is_audio = acodec != 'none'

                resolution = ''
                if is_video and format.get('height'):
                    resolution = f"{format.get('height')}p"

                bitrate = ''
                if is_audio and tbr:
                    bitrate = f"{int(tbr)}k"

                size = ''
                if filesize:
                    size = format_filesize(filesize)

                format_description = f"{ext.upper()}"
                if resolution:
                    format_description += f" {resolution}"
                if bitrate:
                    format_description += f" {bitrate}"
                if size:
                    format_description += f" ({size})"

                format_type = "video" if is_video else "audio"
                if is_video and is_audio:
                    format_type = "video+audio"

                formats.append({
                    'format_id': format_id,
                    'description': format_description,
                    'ext': ext,
                    'resolution': resolution,
                    'bitrate': bitrate,
                    'size': size,
                    'type': format_type
                })

            # Thêm thông tin video
            result = {
                'success': True,
                'title': info.get('title', ''),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats
            }

            return result
    except Exception as e:
        return {'success': False, 'error': str(e)}


def format_filesize(size_bytes):
    """
    Chuyển đổi kích thước file từ bytes sang định dạng đọc được (KB, MB, GB)
    """
    if not size_bytes:
        return ""

    size_bytes = float(size_bytes)
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name)-1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"


def get_content_type(format_type):
    """
    Trả về content type dựa trên định dạng file
    """
    content_types = {
        'mp3': 'audio/mpeg',
        'm4a': 'audio/mp4',
        'opus': 'audio/opus',
        'flac': 'audio/flac',
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'mov': 'video/quicktime',
        'mkv': 'video/x-matroska'
    }
    return content_types.get(format_type, 'application/octet-stream')
