from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')  # Phân quyền: 'customer' hoặc 'admin'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    old_price = db.Column(db.Integer)
    new_price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    sold_count = db.Column(db.Integer, default=0)
    
    # Quan hệ một - nhiều với bảng ảnh (Xóa sản phẩm tự động xóa ảnh đính kèm)
    images = db.relationship('ProductImage', backref='product', cascade="all, delete-orphan", lazy=True)

##### THÊM #####
    # Quan hệ một - nhiều với bảng đánh giá (Xóa sản phẩm tự động xóa đánh giá liên quan)
    reviews = db.relationship('Review', backref='product', cascade="all, delete-orphan", lazy=True)

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(500), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

##### THÊM #####
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) # Số sao (Ví dụ: từ 1 đến 5)
    comment = db.Column(db.Text, nullable=False)  # Nội dung nhận xét
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) # Thời gian đánh giá
    
    # Khóa ngoại liên kết tới bảng Product và User
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Thiết lập mối quan hệ để lấy nhanh tên người đánh giá
    user = db.relationship('User', backref='reviews', lazy=True)