# Cây Cảnh Hà Nội - Web Project

## Hướng dẫn chạy dự án

### Bước 1: Cài đặt thư viện
```bash
pip install -r requirements.txt
```
```bash
pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-Login
```
SQLite
SQLite Viewer

### Bước 2: Chạy ứng dụng
**Trên Windows:**
- Nhấp đôi vào file `run.bat` hoặc chạy lệnh:
```bash
python app.py
```

**Trên Mac/Linux:**
```bash
python3 app.py
```

### Bước 3: Mở ứng dụng
- Mở trình duyệt web
- Truy cập: http://localhost:5000

## Tài khoản mặc định
- **Username:** admin
- **Password:** admin123

## Cấu trúc dự án
```
.
├── app.py                 # File chính của Flask app
├── models.py             # Định nghĩa các model CSDL
├── routes/
│   ├── auth.py          # Route đăng nhập/đăng ký
│   ├── product.py       # Route sản phẩm
│   └── admin.py         # Route quản trị
├── templates/           # Các file HTML template
├── static/              # Các file CSS, JS, hình ảnh
├── requirements.txt     # Danh sách thư viện cần cài
└── database.db         # Cơ sở dữ liệu SQLite (tự tạo)
```

## Các tính năng chính
✓ Đăng nhập/Đăng ký tài khoản  
✓ Xem danh sách sản phẩm cây cảnh  
✓ Tìm kiếm và lọc sản phẩm  
✓ Xem chi tiết sản phẩm  
✓ Quản trị sản phẩm (thêm/sửa/xóa)  
✓ Upload ảnh sản phẩm  
✓ Phân quyền Admin  
✓ Thêm đánh giá sản phẩm

## Ghi chú
- Cơ sở dữ liệu sẽ tự động tạo khi chạy app lần đầu
- Tài khoản Admin mặc định sẽ được tạo tự động
- Folder `/static/uploads` dùng để lưu ảnh sản phẩm
