import os
import uuid
import tempfile
import shutil
import yt_dlp
from django.conf import settings

def download_media(url, format_type, progress_callback=None):
    """
    Hàm download media từ URL với định dạng được chỉ định
    Trả về thông tin về file đã tải xuống hoặc lỗi

    Args:
        url: URL del video a descargar
        format_type: Formato de salida (mp3, mp4, mov)
        progress_callback: Función para reportar el progreso de descarga
    """
    # Tạo thư mục media nếu chưa tồn tại
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    # Tạo thư mục theo định dạng
    media_folder = 'audio' if format_type == 'mp3' else 'video'
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
        'progress_hooks': [progress_hook]
    }

    # Xử lý tùy chọn định dạng
    if format_type == 'mp3':
        options['format'] = 'bestaudio'
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        file_extension = 'mp3'
        content_type = 'audio/mpeg'
    elif format_type == 'mov':
        options['format'] = 'bestvideo[ext=mov]+bestaudio/best[ext=mov]/best'
        file_extension = 'mov'
        content_type = 'video/quicktime'
        # Thêm cấu hình ffmpeg nếu cần chuyển đổi sang mov
        options['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mov',
        }]
    else:  # mp4 (mặc định)
        options['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        file_extension = 'mp4'
        content_type = 'video/mp4'

    try:
        # Download video/audio
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                shutil.rmtree(temp_dir)  # Xóa thư mục tạm
                return {'success': False, 'error': 'Không thể tải video. Vui lòng thử URL hoặc định dạng khác.'}

            title = info.get('title', 'Unknown Title')

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
            'format': format_type
        }

    except Exception as e:
        # Xóa thư mục tạm nếu có lỗi
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return {'success': False, 'error': str(e)}


def get_content_type(format_type):
    """
    Trả về content type dựa trên định dạng file
    """
    if format_type == 'mp3':
        return 'audio/mpeg'
    elif format_type == 'mov':
        return 'video/quicktime'
    else:  # mp4
        return 'video/mp4'
