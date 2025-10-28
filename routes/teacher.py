"""
Маршруты для преподавателя
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import Teacher, Schedule, Group, Subject, LessonTime
from datetime import datetime, timedelta

bp = Blueprint('teacher', __name__, url_prefix='/teacher')

def teacher_required(f):
    """Декоратор для проверки прав преподавателя"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('Доступ запрещен', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """Панель преподавателя"""
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    if not teacher:
        flash('Профиль преподавателя не найден', 'danger')
        return redirect(url_for('index'))
    
    # Расписание на сегодня
    today = datetime.now().date()
    today_schedule = Schedule.query.filter_by(
        teacher_id=teacher.id,
        date=today,
        is_active=True
    ).order_by(Schedule.lesson_time_id).all()
    
    # Расписание на неделю
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_schedule = Schedule.query.filter(
        Schedule.teacher_id == teacher.id,
        Schedule.date >= week_start,
        Schedule.date <= week_end,
        Schedule.is_active == True
    ).order_by(Schedule.date, Schedule.lesson_time_id).all()
    
    return render_template('teacher/dashboard.html',
                         teacher=teacher,
                         today_schedule=today_schedule,
                         week_schedule=week_schedule)

@bp.route('/schedule')
@login_required
@teacher_required
def schedule():
    """Расписание преподавателя"""
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    # Получение параметров фильтрации
    date_str = request.args.get('date')
    if date_str:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()
    
    # Расписание на выбранную дату
    schedules = Schedule.query.filter_by(
        teacher_id=teacher.id,
        date=selected_date,
        is_active=True
    ).order_by(Schedule.lesson_time_id).all()
    
    return render_template('teacher/schedule.html',
                         schedules=schedules,
                         selected_date=selected_date)

@bp.route('/add-lesson', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_lesson():
    """Добавление занятия"""
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        group_id = request.form.get('group_id')
        lesson_time_id = request.form.get('lesson_time_id')
        weekday = request.form.get('weekday')
        lesson_type = request.form.get('lesson_type')
        classroom = request.form.get('classroom')
        date_str = request.form.get('date')
        notes = request.form.get('notes')
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Проверка на конфликты
        conflict = Schedule.query.filter_by(
            group_id=group_id,
            lesson_time_id=lesson_time_id,
            date=date,
            is_active=True
        ).first()
        
        if conflict:
            flash('В это время у группы уже есть занятие', 'danger')
            return redirect(url_for('teacher.add_lesson'))
        
        schedule = Schedule(
            subject_id=subject_id,
            group_id=group_id,
            teacher_id=teacher.id,
            lesson_time_id=lesson_time_id,
            weekday=weekday,
            lesson_type=lesson_type,
            classroom=classroom,
            date=date,
            notes=notes
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        flash('Занятие успешно добавлено', 'success')
        return redirect(url_for('teacher.schedule'))
    
    # Получение данных для формы
    subjects = Subject.query.order_by(Subject.name).all()
    groups = Group.query.order_by(Group.course, Group.name).all()
    lesson_times = LessonTime.query.order_by(LessonTime.lesson_number).all()
    
    return render_template('teacher/add_lesson.html',
                         subjects=subjects,
                         groups=groups,
                         lesson_times=lesson_times)

@bp.route('/edit-lesson/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_lesson(id):
    """Редактирование занятия"""
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    schedule = Schedule.query.get_or_404(id)
    
    # Проверка прав доступа
    if schedule.teacher_id != teacher.id:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('teacher.schedule'))
    
    if request.method == 'POST':
        schedule.subject_id = request.form.get('subject_id')
        schedule.group_id = request.form.get('group_id')
        schedule.lesson_time_id = request.form.get('lesson_time_id')
        schedule.weekday = request.form.get('weekday')
        schedule.lesson_type = request.form.get('lesson_type')
        schedule.classroom = request.form.get('classroom')
        schedule.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        schedule.notes = request.form.get('notes')
        
        db.session.commit()
        
        flash('Занятие успешно обновлено', 'success')
        return redirect(url_for('teacher.schedule'))
    
    subjects = Subject.query.order_by(Subject.name).all()
    groups = Group.query.order_by(Group.course, Group.name).all()
    lesson_times = LessonTime.query.order_by(LessonTime.lesson_number).all()
    
    return render_template('teacher/edit_lesson.html',
                         schedule=schedule,
                         subjects=subjects,
                         groups=groups,
                         lesson_times=lesson_times)

@bp.route('/delete-lesson/<int:id>', methods=['POST'])
@login_required
@teacher_required
def delete_lesson(id):
    """Удаление занятия"""
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    schedule = Schedule.query.get_or_404(id)
    
    if schedule.teacher_id != teacher.id:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('teacher.schedule'))
    
    db.session.delete(schedule)
    db.session.commit()
    
    flash('Занятие удалено', 'success')
    return redirect(url_for('teacher.schedule'))

@bp.route('/groups')
@login_required
@teacher_required
def groups():
    """Список групп преподавателя"""
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    # Получение уникальных групп из расписания
    teacher_groups = db.session.query(Group).join(Schedule).filter(
        Schedule.teacher_id == teacher.id
    ).distinct().order_by(Group.course, Group.name).all()
    
    return render_template('teacher/groups.html', groups=teacher_groups)
