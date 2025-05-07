# YouTube AI Downloader

Ứng dụng web Django cho phép tải xuống video và âm thanh từ YouTube.

## Tính năng

- Tải xuống video từ YouTube với nhiều định dạng
- Trích xuất âm thanh từ video dưới dạng MP3
- Xem trước nội dung video trước khi tải xuống
- Hệ thống đăng nhập và đăng ký người dùng
- Lưu lịch sử tải xuống của người dùng

## Yêu cầu

- Python 3.8+
- Django 4.2.7
- yt-dlp 2023.7.6
- FFmpeg
- Các thư viện khác được liệt kê trong requirements.txt

## Cài đặt

1. Clone repository:
   ```
   git clone https://github.com/yourusername/youtube-ai.git
   cd youtube-ai
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
youtube-ai/
├── downloader/              # Ứng dụng tải xuống video YouTube
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files cho downloader
│   ├── templates/           # HTML templates
│   ├── admin.py             # Cấu hình admin
│   ├── apps.py              # Cấu hình ứng dụng
│   ├── forms.py             # Form tải xuống
│   ├── models.py            # Model lưu lịch sử tải xuống
│   ├── tests.py             # Unit tests
│   ├── urls.py              # URL routing
│   ├── utils.py             # Các hàm tiện ích để tải video
│   └── views.py             # Views xử lý tải xuống
│
├── user_auth/               # Ứng dụng xác thực người dùng
│   ├── migrations/
│   ├── templates/           # Templates đăng nhập/đăng ký
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py             # Forms đăng nhập/đăng ký
│   ├── models.py            # Mô hình người dùng
│   ├── tests.py
│   ├── urls.py              # URL routing xác thực
│   └── views.py             # Views xác thực
│
├── youtube_downloader/      # Cấu hình chính của dự án
│   ├── asgi.py
│   ├── settings.py          # Cài đặt dự án
│   ├── urls.py              # URL routing chính
│   └── wsgi.py
│
├── static/                  # Static files chung
│
├── media/                   # Thư mục lưu file tải xuống
│
├── db.sqlite3               # Cơ sở dữ liệu SQLite
├── manage.py                # Script quản lý Django
├── requirements.txt         # Danh sách thư viện cần thiết
└── README.md
```

## Cách sử dụng

1. Đăng ký tài khoản hoặc đăng nhập nếu đã có tài khoản
2. Nhập URL video YouTube vào form
3. Chọn định dạng tải xuống (video hoặc âm thanh)
4. Nhấn nút "Tải xuống" và đợi quá trình hoàn tất
5. File được tải xuống sẽ có sẵn trong trình duyệt để lưu về máy

## Đóng góp

Vui lòng gửi Pull Request hoặc báo cáo lỗi qua phần Issues.

## License

MIT

## Tác giả

Your Name
