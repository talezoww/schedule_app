"""
Общие маршруты для расписания
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models import Schedule, LessonTime
from datetime import datetime

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/api/lesson-times')
@login_required
def api_lesson_times():
    """API для получения расписания звонков"""
    times = LessonTime.query.order_by(LessonTime.lesson_number).all()
    return jsonify([{
        'id': t.id,
        'lesson_number': t.lesson_number,
        'hour_number': t.hour_number,
        'start_time': t.start_time.strftime('%H:%M'),
        'end_time': t.end_time.strftime('%H:%M')
    } for t in times])

@bp.route('/api/schedule/<int:group_id>/<date>')
@login_required
def api_schedule(group_id, date):
    """API для получения расписания группы на дату"""
    try:
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    schedules = Schedule.query.filter_by(
        group_id=group_id,
        date=selected_date,
        is_active=True
    ).order_by(Schedule.lesson_time_id).all()
    
    return jsonify([{
        'id': s.id,
        'subject': s.subject.name,
        'teacher': s.teacher.user.get_full_name(),
        'lesson_time': s.lesson_time.get_time_range(),
        'lesson_type': s.get_lesson_type_display(),
        'classroom': s.classroom,
        'notes': s.notes
    } for s in schedules])
