from django.shortcuts import render, redirect
import os
import json
import threading
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from .forms import DownloadForm
from .models import Download
from .utils import download_media, get_content_type

# Diccionario global para almacenar el progreso de descarga
download_progress = {}

def home(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            format_type = form.cleaned_data['format']

            # Generar un ID de descarga temporal
            import uuid
            download_id = str(uuid.uuid4())
            download_progress[download_id] = 0

            # Iniciar descarga en un hilo secundario
            thread = threading.Thread(
                target=process_download,
                args=(url, format_type, download_id, request)
            )
            thread.daemon = True
            thread.start()

            # Si es una solicitud AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'download_id': download_id
                })

            # Si es una solicitud normal, redirigir a la página de progreso
            return redirect('downloader:progress', download_id=download_id)
    else:
        form = DownloadForm()

    # Lấy lịch sử download gần đây
    recent_downloads = Download.objects.order_by('-created_at')[:5]

    return render(request, 'downloader/home.html', {
        'form': form,
        'recent_downloads': recent_downloads
    })

def download_progress_page(request, download_id):
    """Muestra la página con el progreso de la descarga"""
    if download_id not in download_progress:
        return render(request, 'downloader/error.html', {
            'error': 'Không tìm thấy ID tải xuống. Nó có thể đã hoàn thành hoặc bị hủy.'
        })

    return render(request, 'downloader/progress.html', {
        'download_id': download_id
    })

def process_download(url, format_type, download_id, request):
    """Procesa la descarga en un hilo separado y actualiza el progreso"""
    try:
        result = download_media(url, format_type, progress_callback=lambda progress: update_progress(download_id, progress))

        if not result['success']:
            download_progress[download_id] = {
                'status': 'error',
                'error': result['error']
            }
            return

        # Lưu thông tin download vào database với đường dẫn file
        download = Download.objects.create(
            url=url,
            title=result['title'],
            format=format_type,
            file_path=result['file_path']
        )

        # Actualizar progreso con información de éxito
        download_progress[download_id] = {
            'status': 'completed',
            'download_db_id': download.id
        }
    except Exception as e:
        download_progress[download_id] = {
            'status': 'error',
            'error': str(e)
        }

def update_progress(download_id, progress):
    """Actualiza el progreso de descarga"""
    download_progress[download_id] = {
        'status': 'downloading',
        'progress': progress
    }

@csrf_exempt
def get_download_progress(request, download_id):
    """Devuelve el progreso actual de la descarga"""
    if download_id not in download_progress:
        return JsonResponse({
            'status': 'not_found'
        }, status=404)

    progress_data = download_progress[download_id]

    # Si la descarga está completa, limpiar el progreso después de un tiempo
    if isinstance(progress_data, dict) and progress_data.get('status') == 'completed':
        # Programar eliminación del progreso después de un tiempo
        download_db_id = progress_data.get('download_db_id')
        threading.Timer(300, lambda: download_progress.pop(download_id, None)).start()

        return JsonResponse({
            'status': 'completed',
            'download_id': download_db_id
        })

    return JsonResponse(progress_data if isinstance(progress_data, dict) else {
        'status': 'downloading',
        'progress': progress_data
    })

def download_history(request):
    downloads = Download.objects.order_by('-created_at')
    return render(request, 'downloader/history.html', {'downloads': downloads})

def preview_media(request, download_id):
    try:
        download = Download.objects.get(id=download_id)
        if not download.file_path:
            return render(request, 'downloader/error.html', {'error': 'File không tồn tại.'})

        file_path = os.path.join(settings.MEDIA_ROOT, download.file_path)
        if not os.path.exists(file_path):
            return render(request, 'downloader/error.html', {'error': 'File không tồn tại trên server.'})

        return render(request, 'downloader/preview.html', {'download': download})
    except Download.DoesNotExist:
        return render(request, 'downloader/error.html', {'error': 'Không tìm thấy bản ghi download.'})

def download_file(request, download_id):
    try:
        download = Download.objects.get(id=download_id)
        if not download.file_path:
            return render(request, 'downloader/error.html', {'error': 'File không tồn tại.'})

        file_path = os.path.join(settings.MEDIA_ROOT, download.file_path)
        if not os.path.exists(file_path):
            return render(request, 'downloader/error.html', {'error': 'File không tồn tại trên server.'})

        # Crear un nombre de archivo amigable basado en el título
        safe_title = "".join([c for c in download.title if c.isalpha() or c.isdigit() or c==' ']).strip()
        safe_title = safe_title.replace(' ', '_')
        # Obtener la extensión del archivo
        file_extension = os.path.splitext(download.file_path)[1] or f'.{download.format}'
        download_filename = f"{safe_title}{file_extension}"

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            response['Content-Type'] = get_content_type(download.format)
            response['Content-Disposition'] = f'attachment; filename="{download_filename}"'
            return response
    except Download.DoesNotExist:
        return render(request, 'downloader/error.html', {'error': 'Không tìm thấy bản ghi download.'})

def serve_media_file(request, download_id):
    try:
        download = Download.objects.get(id=download_id)
        if not download.file_path:
            return HttpResponse(status=404)

        file_path = os.path.join(settings.MEDIA_ROOT, download.file_path)
        if not os.path.exists(file_path):
            return HttpResponse(status=404)

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            response['Content-Type'] = get_content_type(download.format)
            # Bỏ Content-Disposition để cho phép xem trực tiếp trong trình duyệt
            return response
    except Download.DoesNotExist:
        return HttpResponse(status=404)

# API Endpoints cho thêm, sửa, xóa
@require_POST
@csrf_exempt
def delete_download(request, download_id):
    try:
        download = Download.objects.get(id=download_id)

        # Xóa file nếu tồn tại
        if download.file_path:
            file_path = os.path.join(settings.MEDIA_ROOT, download.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Xóa bản ghi từ database
        download.delete()

        return JsonResponse({
            'success': True,
            'message': 'Đã xóa file thành công'
        })
    except Download.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy bản ghi download'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_http_methods(["GET", "POST"])
def edit_download(request, download_id):
    try:
        download = Download.objects.get(id=download_id)

        if request.method == 'GET':
            # Trả về form chỉnh sửa
            return render(request, 'downloader/edit.html', {'download': download})

        elif request.method == 'POST':
            # Cập nhật thông tin
            title = request.POST.get('title')
            if title:
                download.title = title
                download.save()

            return redirect('downloader:preview', download_id=download.id)

    except Download.DoesNotExist:
        return render(request, 'downloader/error.html', {
            'error': 'Không tìm thấy bản ghi download'
        })

@require_http_methods(["GET", "POST"])
@csrf_exempt
def api_update_download(request, download_id):
    try:
        download = Download.objects.get(id=download_id)

        if request.method == 'GET':
            # Trả về thông tin download dưới dạng JSON
            return JsonResponse({
                'id': download.id,
                'url': download.url,
                'title': download.title,
                'format': download.format,
                'created_at': download.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        elif request.method == 'POST':
            # Đọc dữ liệu JSON từ request body
            data = json.loads(request.body)
            title = data.get('title')

            if title:
                download.title = title
                download.save()

                return JsonResponse({
                    'success': True,
                    'download': {
                        'id': download.id,
                        'url': download.url,
                        'title': download.title,
                        'format': download.format,
                        'created_at': download.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Thiếu thông tin cần thiết'
                }, status=400)

    except Download.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy bản ghi download'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu JSON không hợp lệ'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Create your views here.
