from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'downloader'

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.download_history, name='history'),
    path('preview/<int:download_id>/', views.preview_media, name='preview'),
    path('download/<int:download_id>/', views.download_file, name='download_file'),
    path('media/<int:download_id>/', views.serve_media_file, name='media_file'),
    path('progress/<str:download_id>/', views.download_progress_page, name='progress'),

    # API endpoints
    path('api/download/<int:download_id>/delete/', views.delete_download, name='api_delete'),
    path('download/<int:download_id>/edit/', views.edit_download, name='edit'),
    path('api/download/<int:download_id>/update/', views.api_update_download, name='api_update'),
    path('api/download-progress/<str:download_id>/', views.get_download_progress, name='download_progress'),
    path('api/get-formats/', views.get_available_formats_api, name='get_formats'),
]
