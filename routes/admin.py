import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Product, ProductImage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not is_admin(): 
        return "Bạn không có quyền truy cập trang này!", 403
    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)

@admin_bp.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not is_admin(): 
        return "Từ chối truy cập!", 403
    
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        new_price = int(request.form.get('new_price'))
        old_price = int(request.form.get('old_price')) if request.form.get('old_price') else None
        description = request.form.get('description')
        
        product = Product(name=name, category=category, new_price=new_price, old_price=old_price, description=description)
        db.session.add(product)
        db.session.commit()
        
        # Xử lý tính năng nâng cao: Upload nhiều ảnh cùng lúc
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                
                img_record = ProductImage(image_url=f'uploads/{filename}', product_id=product.id)
                db.session.add(img_record)
                
        db.session.commit()
        flash('Đã thêm cây cảnh mới thành công!')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/product_form.html', product=None)

@admin_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not is_admin(): 
        return "Từ chối truy cập!", 403
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.new_price = int(request.form.get('new_price'))
        product.old_price = int(request.form.get('old_price')) if request.form.get('old_price') else None
        product.description = request.form.get('description')
        
        db.session.commit()
        flash('Đã cập nhật thông tin cây cảnh!')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/product_form.html', product=product)

@admin_bp.route('/product/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    if not is_admin(): 
        return "Từ chối truy cập!", 403
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Đã xóa sản phẩm thành công!')
    return redirect(url_for('admin.dashboard'))