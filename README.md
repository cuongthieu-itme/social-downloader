# YouTube AI Downloader

Ứng dụng web Django cho phép tải xuống video và âm thanh từ YouTube.

## Tính năng

- Tải xuống video từ YouTube với nhiều định dạng
- Trích xuất âm thanh từ video dưới dạng MP3
- Xem trước nội dung video trước khi tải xuống
- Lưu lịch sử tải xuống
- Quản lý và chỉnh sửa video đã tải xuống

## Yêu cầu

- Python 3.8+
- Django 4.2.7
- yt-dlp
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

6. Tạo tài khoản admin (tùy chọn):
   ```
   python manage.py createsuperuser
   ```

7. Chạy server:
   ```
   python manage.py runserver
   ```

## Deployment lên Render

1. Đăng ký tài khoản trên [Render](https://render.com)

2. Tạo file cấu hình cần thiết (đã có trong repo):
   - `build.sh`: Script cài đặt
   - `Procfile`: Định nghĩa cách chạy ứng dụng
   - Cập nhật `settings.py` để hỗ trợ môi trường production
   - Tạo file `.env` từ mẫu `.env-sample`

3. Trong trang Dashboard của Render:
   - Chọn "New" > "Web Service"
   - Kết nối với GitHub và chọn repository của bạn
   - Đặt tên cho ứng dụng
   - Chọn "Python" làm Runtime
   - Đảm bảo Build Command là `./build.sh` và Start Command là `gunicorn youtube_downloader.wsgi`
   - Chọn Free plan hoặc paid plan tùy nhu cầu

4. Thiết lập các biến môi trường (Environment Variables):
   - `SECRET_KEY`: Khóa bí mật cho Django
   - `DEBUG`: Đặt là `False` cho môi trường production
   - `ALLOWED_HOSTS`: Thêm tên miền ứng dụng của bạn trên Render

5. Nhấn "Create Web Service" và đợi deployment hoàn tất

6. Đối với FFmpeg:
   - Render cần cấu hình thêm cho FFmpeg.
   - Thêm vào Advanced Settings > Startup Command:
   ```bash
   apt-get update && apt-get install -y ffmpeg && gunicorn youtube_downloader.wsgi
   ```

7. Sau khi deployment thành công, ứng dụng của bạn sẽ có sẵn tại URL được cung cấp

## Cấu trúc dự án

```
youtube-ai/
├── downloader/              # Ứng dụng tải xuống video YouTube
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files cho downloader
│   ├── templates/           # HTML templates
│   │   └── downloader/      # Template cho các trang của ứng dụng
│   │       ├── base.html    # Template cơ sở
│   │       ├── home.html    # Trang chủ/tải xuống
│   │       ├── preview.html # Xem trước video
│   │       ├── progress.html# Theo dõi tiến trình tải xuống
│   │       ├── history.html # Lịch sử tải xuống
│   │       ├── edit.html    # Chỉnh sửa video
│   │       └── error.html   # Trang thông báo lỗi
│   ├── admin.py             # Cấu hình admin
│   ├── apps.py              # Cấu hình ứng dụng
│   ├── forms.py             # Form tải xuống và xử lý
│   ├── models.py            # Model lưu lịch sử tải xuống
│   ├── tests.py             # Unit tests
│   ├── urls.py              # URL routing
│   ├── utils.py             # Các hàm tiện ích để tải video
│   └── views.py             # Views xử lý tải xuống
│
├── youtube_downloader/      # Cấu hình chính của dự án
│   ├── asgi.py              # ASGI config
│   ├── settings.py          # Cài đặt dự án
│   ├── urls.py              # URL routing chính
│   └── wsgi.py              # WSGI config
│
├── static/                  # Static files chung (CSS, JS, Images)
│
├── media/                   # Thư mục lưu file tải xuống
│
├── db.sqlite3               # Cơ sở dữ liệu SQLite
├── manage.py                # Script quản lý Django
├── requirements.txt         # Danh sách thư viện cần thiết
└── README.md                # Tài liệu dự án
```

## Cách sử dụng

1. Truy cập trang chủ của ứng dụng
2. Nhập URL video YouTube vào form
3. Chọn định dạng tải xuống (video hoặc âm thanh)
4. Nhấn nút "Tải xuống" và đợi quá trình hoàn tất
5. File được tải xuống sẽ có sẵn để lưu về máy
6. Xem và quản lý lịch sử tải xuống trong phần "Lịch sử"

## Các chức năng chính

### Tải xuống video
- Hỗ trợ nhiều định dạng video (mp4, webm)
- Tùy chọn chất lượng video (360p, 720p, 1080p, ...)

### Tải xuống âm thanh
- Trích xuất âm thanh từ video dưới dạng mp3
- Tùy chọn chất lượng âm thanh

### Xem trước
- Xem thông tin video trước khi tải xuống
- Kiểm tra video có sẵn cho tải xuống hay không

### Lịch sử tải xuống
- Theo dõi video đã tải xuống trước đó
- Xem, quản lý và tải xuống lại video từ lịch sử

## Đóng góp

Vui lòng gửi Pull Request hoặc báo cáo lỗi qua phần Issues.

## License

MIT

## Tác giả

Your Name
