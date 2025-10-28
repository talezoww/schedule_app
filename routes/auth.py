"""
Маршруты аутентификации
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, PendingUser, Group

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Вход в систему"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            if user.is_active:
                login_user(user, remember=request.form.get('remember', False))
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Ваш аккаунт деактивирован', 'danger')
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        role = request.form.get('role')  # student или teacher
        
        # Валидация
        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Имя пользователя уже занято', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'danger')
            return redirect(url_for('auth.register'))
        
        # Создание запроса на регистрацию
        pending_user = PendingUser(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            requested_role=role
        )
        
        # Дополнительные поля для студентов
        if role == 'student':
            pending_user.group_id = request.form.get('group_id')
            pending_user.course = request.form.get('course')
        
        # Дополнительные поля для преподавателей
        if role == 'teacher':
            pending_user.department = request.form.get('department')
            pending_user.position = request.form.get('position')
        
        db.session.add(pending_user)
        db.session.commit()
        
        flash('Заявка на регистрацию отправлена. Ожидайте подтверждения администратора.', 'success')
        return redirect(url_for('auth.login'))
    
    # Получение списка групп для формы
    groups = Group.query.order_by(Group.course, Group.name).all()
    return render_template('auth/register.html', groups=groups)

@bp.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('auth.login'))
