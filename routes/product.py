from flask import Blueprint, render_template, request, redirect, url_for, flash
##### THÊM #####
from flask_login import login_required, current_user
from models import db, Product, Review

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def index():
    query = request.args.get('search', '')
    category_filter = request.args.get('category', '')

    products_query = Product.query
    if query:
        products_query = products_query.filter(Product.name.like(f'%{query}%'))
    if category_filter:
        products_query = products_query.filter(Product.category == category_filter)

    products = products_query.all()
    return render_template('index.html', products=products, search=query, category=category_filter)

@product_bp.route('/product/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    
    tiet_kiem = 0
    phan_tram = 0
    if product.old_price and product.old_price > product.new_price:
        tiet_kiem = product.old_price - product.new_price
        phan_tram = int((tiet_kiem / product.old_price) * 100)

##### BỎ DÒNG NÀY #####        
    # return render_template('product_detail.html', product=product, tiet_kiem=tiet_kiem, phan_tram_giam=phan_tram)

##### THÊM #####
# Lấy tất cả đánh giá của sản phẩm này, xếp mới nhất lên đầu
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    
    # Tính điểm trung bình số sao (nếu có đánh giá)
    avg_rating = 0
    if reviews:
        avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)

    return render_template('product_detail.html', 
                           product=product, 
                           tiet_kiem=tiet_kiem, 
                           phan_tram_giam=phan_tram,
                           reviews=reviews,
                           avg_rating=avg_rating)

# 2. Thêm route mới để xử lý khi bấm nút "Gửi đánh giá"
@product_bp.route('/product/<int:product_id>/review', methods=['POST'])
@login_required # Chỉ cho phép người dùng đã đăng nhập đánh giá
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if rating and comment:
        new_review = Review(
            rating=int(rating),
            comment=comment,
            product_id=product.id,
            user_id=current_user.id
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Cảm ơn bạn đã gửi đánh giá sản phẩm!')
    else:
        flash('Vui lòng điền đầy đủ số sao và nội dung đánh giá.')
        
    return redirect(url_for('product.detail', product_id=product.id))