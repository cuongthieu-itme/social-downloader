# YouTube Downloader

Ứng dụng web Django cho phép tải xuống video và âm thanh từ YouTube và các trang web khác.

## Tính năng

- Tải xuống video từ YouTube với nhiều định dạng (MP4, MOV)
- Trích xuất âm thanh từ video dưới dạng MP3
- Xem trước video/âm thanh trong trình duyệt
- Lưu lịch sử tải xuống
- Quản lý tài khoản người dùng

## Yêu cầu

- Python 3.8+
- Django 4.2+
- yt-dlp
- FFmpeg

## Cài đặt

1. Clone repository:
   ```
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   ```

2. Tạo và kích hoạt môi trường ảo:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Cài đặt các gói phụ thuộc:
   ```
   pip install -r requirements.txt
   ```

4. Cài đặt FFmpeg:
   - Linux: `sudo apt install ffmpeg`
   - MacOS: `brew install ffmpeg`
   - Windows: Tải từ https://ffmpeg.org/download.html

5. Thực hiện migrations:
   ```
   python manage.py migrate
   ```

6. Tạo tài khoản admin:
   ```
   python manage.py createsuperuser
   ```

7. Chạy server:
   ```
   python manage.py runserver
   ```

## Cấu trúc dự án

```
youtube_downloader/
├── downloader/              # Ứng dụng chính cho tải xuống
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files cho ứng dụng downloader
│   │   └── downloader/
│   │       ├── css/         # CSS files
│   │       ├── js/          # JavaScript files
│   │       └── img/         # Hình ảnh
│   ├── templates/           # HTML templates
│   │   └── downloader/
│   ├── __init__.py
│   ├── admin.py             # Cấu hình admin
│   ├── apps.py              # Cấu hình ứng dụng
│   ├── forms.py             # Các form
│   ├── models.py            # Mô hình dữ liệu
│   ├── tests.py             # Unit tests
│   ├── urls.py              # URL routing
│   ├── utils.py             # Tiện ích và hàm hỗ trợ
│   └── views.py             # Views
│
├── user_auth/               # Ứng dụng quản lý người dùng
│   ├── migrations/
│   ├── templates/
│   │   └── user_auth/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── youtube_downloader/      # Cấu hình dự án
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/                  # Static files chung
│   ├── css/
│   ├── js/
│   └── img/
│
├── media/                   # Media files (uploaded and downloaded)
│   ├── audio/               # Audio files (MP3)
│   ├── video/               # Video files (MP4, MOV)
│   └── avatars/             # User avatars
│
├── staticfiles/             # Collected static files
├── manage.py
├── requirements.txt
└── README.md
```

## License

MIT

## Tác giả

Your Name
