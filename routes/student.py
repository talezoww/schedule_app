"""
Маршруты для студента
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import Student, Schedule, Note, LessonTime
from datetime import datetime, timedelta

bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    """Декоратор для проверки прав студента"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('Доступ запрещен', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Панель студента"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if not student:
        flash('Профиль студента не найден', 'danger')
        return redirect(url_for('index'))
    
    # Расписание на сегодня
    today = datetime.now().date()
    today_schedule = Schedule.query.filter_by(
        group_id=student.group_id,
        date=today,
        is_active=True
    ).order_by(Schedule.lesson_time_id).all()
    
    # Расписание на неделю
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_schedule = Schedule.query.filter(
        Schedule.group_id == student.group_id,
        Schedule.date >= week_start,
        Schedule.date <= week_end,
        Schedule.is_active == True
    ).order_by(Schedule.date, Schedule.lesson_time_id).all()
    
    return render_template('student/dashboard.html',
                         student=student,
                         today_schedule=today_schedule,
                         week_schedule=week_schedule)

@bp.route('/schedule')
@login_required
@student_required
def schedule():
    """Расписание студента"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    # Получение параметров фильтрации
    view_type = request.args.get('view', 'day')  # day, week, month
    date_str = request.args.get('date')
    
    if date_str:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()
    
    schedules = []
    
    if view_type == 'day':
        schedules = Schedule.query.filter_by(
            group_id=student.group_id,
            date=selected_date,
            is_active=True
        ).order_by(Schedule.lesson_time_id).all()
    
    elif view_type == 'week':
        week_start = selected_date - timedelta(days=selected_date.weekday())
        week_end = week_start + timedelta(days=6)
        schedules = Schedule.query.filter(
            Schedule.group_id == student.group_id,
            Schedule.date >= week_start,
            Schedule.date <= week_end,
            Schedule.is_active == True
        ).order_by(Schedule.date, Schedule.lesson_time_id).all()
    
    elif view_type == 'month':
        month_start = selected_date.replace(day=1)
        if selected_date.month == 12:
            month_end = selected_date.replace(year=selected_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = selected_date.replace(month=selected_date.month + 1, day=1) - timedelta(days=1)
        
        schedules = Schedule.query.filter(
            Schedule.group_id == student.group_id,
            Schedule.date >= month_start,
            Schedule.date <= month_end,
            Schedule.is_active == True
        ).order_by(Schedule.date, Schedule.lesson_time_id).all()
    
    return render_template('student/schedule.html',
                         schedules=schedules,
                         selected_date=selected_date,
                         view_type=view_type)

@bp.route('/lesson-times')
@login_required
@student_required
def lesson_times():
    """Расписание звонков"""
    times = LessonTime.query.order_by(LessonTime.lesson_number).all()
    return render_template('student/lesson_times.html', times=times)

@bp.route('/notes')
@login_required
@student_required
def notes():
    """Заметки студента"""
    student_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
    return render_template('student/notes.html', notes=student_notes)

@bp.route('/add-note/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
@student_required
def add_note(schedule_id):
    """Добавление заметки к занятию"""
    schedule = Schedule.query.get_or_404(schedule_id)
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    # Проверка, что занятие относится к группе студента
    if schedule.group_id != student.group_id:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('student.schedule'))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        note = Note(
            user_id=current_user.id,
            schedule_id=schedule_id,
            content=content
        )
        
        db.session.add(note)
        db.session.commit()
        
        flash('Заметка добавлена', 'success')
        return redirect(url_for('student.notes'))
    
    return render_template('student/add_note.html', schedule=schedule)

@bp.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
@student_required
def edit_note(id):
    """Редактирование заметки"""
    note = Note.query.get_or_404(id)
    
    # Проверка прав доступа
    if note.user_id != current_user.id:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('student.notes'))
    
    if request.method == 'POST':
        note.content = request.form.get('content')
        db.session.commit()
        
        flash('Заметка обновлена', 'success')
        return redirect(url_for('student.notes'))
    
    return render_template('student/edit_note.html', note=note)

@bp.route('/delete-note/<int:id>', methods=['POST'])
@login_required
@student_required
def delete_note(id):
    """Удаление заметки"""
    note = Note.query.get_or_404(id)
    
    if note.user_id != current_user.id:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('student.notes'))
    
    db.session.delete(note)
    db.session.commit()
    
    flash('Заметка удалена', 'success')
    return redirect(url_for('student.notes'))

@bp.route('/teachers')
@login_required
@student_required
def teachers():
    """Список преподавателей"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    # Получение уникальных преподавателей из расписания группы
    from models import Teacher
    student_teachers = db.session.query(Teacher).join(Schedule).filter(
        Schedule.group_id == student.group_id
    ).distinct().all()
    
    return render_template('student/teachers.html', teachers=student_teachers)
