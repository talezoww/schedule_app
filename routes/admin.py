"""
Маршруты для администратора
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.security import generate_password_hash
from extensions import db
from models import User, PendingUser, Group, Subject, Teacher, Student, Schedule, LessonTime
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Доступ запрещен', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Панель администратора"""
    pending_count = PendingUser.query.count()
    users_count = User.query.count()
    groups_count = Group.query.count()
    subjects_count = Subject.query.count()
    
    return render_template('admin/dashboard.html',
                         pending_count=pending_count,
                         users_count=users_count,
                         groups_count=groups_count,
                         subjects_count=subjects_count)

@bp.route('/pending-users')
@login_required
@admin_required
def pending_users():
    """Список ожидающих подтверждения пользователей"""
    pending = PendingUser.query.order_by(PendingUser.created_at.desc()).all()
    return render_template('admin/pending_users.html', pending=pending)

@bp.route('/approve-user/<int:id>', methods=['POST'])
@login_required
@admin_required
def approve_user(id):
    """Подтверждение регистрации пользователя"""
    pending = PendingUser.query.get_or_404(id)
    
    # Получение данных из формы
    role = request.form.get('role', pending.requested_role)
    group_id = request.form.get('group_id')
    course = request.form.get('course')
    
    # Создание пользователя
    user = User(
        username=pending.username,
        email=pending.email,
        password_hash=pending.password_hash,
        first_name=pending.first_name,
        last_name=pending.last_name,
        phone=pending.phone,
        role=role
    )
    db.session.add(user)
    db.session.flush()
    
    # Создание профиля в зависимости от роли
    if role == 'student':
        student = Student(
            user_id=user.id,
            student_id=f'STU{user.id:06d}',
            group_id=group_id or pending.group_id,
            enrollment_year=datetime.now().year
        )
        db.session.add(student)
    
    elif role == 'teacher':
        teacher = Teacher(
            user_id=user.id,
            department=pending.department or 'Не указано',
            position=pending.position or 'Преподаватель'
        )
        db.session.add(teacher)
    
    # Удаление заявки
    db.session.delete(pending)
    db.session.commit()
    
    flash(f'Пользователь {user.username} успешно подтвержден', 'success')
    return redirect(url_for('admin.pending_users'))

@bp.route('/reject-user/<int:id>', methods=['POST'])
@login_required
@admin_required
def reject_user(id):
    """Отклонение регистрации пользователя"""
    pending = PendingUser.query.get_or_404(id)
    db.session.delete(pending)
    db.session.commit()
    
    flash('Заявка отклонена', 'info')
    return redirect(url_for('admin.pending_users'))

@bp.route('/users')
@login_required
@admin_required
def users():
    """Список всех пользователей"""
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)

@bp.route('/user/<int:id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(id):
    """Активация/деактивация пользователя"""
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'активирован' if user.is_active else 'деактивирован'
    flash(f'Пользователь {user.username} {status}', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/groups')
@login_required
@admin_required
def groups():
    """Список групп"""
    all_groups = Group.query.order_by(Group.course, Group.name).all()
    return render_template('admin/groups.html', groups=all_groups)

@bp.route('/group/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_group():
    """Добавление новой группы"""
    if request.method == 'POST':
        name = request.form.get('name')
        course = request.form.get('course')
        
        if Group.query.filter_by(name=name).first():
            flash('Группа с таким названием уже существует', 'danger')
            return redirect(url_for('admin.add_group'))
        
        group = Group(name=name, course=course)
        db.session.add(group)
        db.session.commit()
        
        flash(f'Группа {name} успешно создана', 'success')
        return redirect(url_for('admin.groups'))
    
    return render_template('admin/add_group.html')

@bp.route('/group/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_group(id):
    """Удаление группы"""
    group = Group.query.get_or_404(id)
    
    if group.students:
        flash('Невозможно удалить группу со студентами', 'danger')
        return redirect(url_for('admin.groups'))
    
    db.session.delete(group)
    db.session.commit()
    
    flash('Группа удалена', 'success')
    return redirect(url_for('admin.groups'))

@bp.route('/subjects')
@login_required
@admin_required
def subjects():
    """Список предметов"""
    all_subjects = Subject.query.order_by(Subject.name).all()
    return render_template('admin/subjects.html', subjects=all_subjects)

@bp.route('/subject/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_subject():
    """Добавление нового предмета"""
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        description = request.form.get('description')
        hours = request.form.get('hours', 0)
        
        if Subject.query.filter_by(code=code).first():
            flash('Предмет с таким кодом уже существует', 'danger')
            return redirect(url_for('admin.add_subject'))
        
        subject = Subject(name=name, code=code, description=description, hours=hours)
        db.session.add(subject)
        db.session.commit()
        
        flash(f'Предмет {name} успешно создан', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/add_subject.html')

@bp.route('/lesson-times')
@login_required
@admin_required
def lesson_times():
    """Расписание звонков"""
    times = LessonTime.query.order_by(LessonTime.lesson_number).all()
    return render_template('admin/lesson_times.html', times=times)

@bp.route('/lesson-time/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_lesson_time(id):
    """Редактирование времени пары"""
    lesson_time = LessonTime.query.get_or_404(id)
    
    if request.method == 'POST':
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        lesson_time.start_time = datetime.strptime(start_time, '%H:%M').time()
        lesson_time.end_time = datetime.strptime(end_time, '%H:%M').time()
        
        db.session.commit()
        flash('Время пары обновлено', 'success')
        return redirect(url_for('admin.lesson_times'))
    
    return render_template('admin/edit_lesson_time.html', lesson_time=lesson_time)
