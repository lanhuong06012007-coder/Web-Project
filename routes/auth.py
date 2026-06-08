from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Tên tài khoản này đã tồn tại trên hệ thống!')
            return redirect(url_for('auth.register'))
            
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw, role='customer')
        db.session.add(new_user)
        db.session.commit()
        flash('Đăng ký thành công! Mời bạn đăng nhập.')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html', form_type='register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('product.index'))
            
        flash('Tên đăng nhập hoặc mật khẩu không chính xác!')
    return render_template('login.html', form_type='login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('product.index'))