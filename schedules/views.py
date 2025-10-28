from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Schedule, LessonTime, Note, ChangeRequest
from accounts.models import StudentProfile


@login_required
def schedule_day_view(request):
    """Расписание на день"""
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    
    if request.user.is_student():
        try:
            student_profile = request.user.student_profile
            schedules = Schedule.objects.filter(
                group=student_profile.group,
                date=selected_date,
                is_active=True
            ).select_related('subject', 'teacher__user', 'lesson_time').order_by('lesson_time__lesson_number')
        except StudentProfile.DoesNotExist:
            schedules = []
    elif request.user.is_teacher():
        try:
            teacher_profile = request.user.teacher_profile
            schedules = Schedule.objects.filter(
                teacher=teacher_profile,
                date=selected_date,
                is_active=True
            ).select_related('subject', 'group', 'lesson_time').order_by('lesson_time__lesson_number')
        except:
            schedules = []
    else:
        schedules = Schedule.objects.filter(
            date=selected_date,
            is_active=True
        ).select_related('subject', 'group', 'teacher__user', 'lesson_time').order_by('lesson_time__lesson_number')
    
    context = {
        'schedules': schedules,
        'selected_date': selected_date,
        'prev_date': selected_date - timedelta(days=1),
        'next_date': selected_date + timedelta(days=1),
    }
    return render(request, 'schedules/schedule_day.html', context)


@login_required
def schedule_week_view(request):
    """Расписание на неделю"""
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    
    # Начало недели (понедельник)
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    if request.user.is_student():
        try:
            student_profile = request.user.student_profile
            schedules = Schedule.objects.filter(
                group=student_profile.group,
                date__range=[start_of_week, end_of_week],
                is_active=True
            ).select_related('subject', 'teacher__user', 'lesson_time').order_by('date', 'lesson_time__lesson_number')
        except StudentProfile.DoesNotExist:
            schedules = []
    elif request.user.is_teacher():
        try:
            teacher_profile = request.user.teacher_profile
            schedules = Schedule.objects.filter(
                teacher=teacher_profile,
                date__range=[start_of_week, end_of_week],
                is_active=True
            ).select_related('subject', 'group', 'lesson_time').order_by('date', 'lesson_time__lesson_number')
        except:
            schedules = []
    else:
        schedules = Schedule.objects.filter(
            date__range=[start_of_week, end_of_week],
            is_active=True
        ).select_related('subject', 'group', 'teacher__user', 'lesson_time').order_by('date', 'lesson_time__lesson_number')
    
    # Группировка по дням
    schedule_by_day = {}
    for schedule in schedules:
        if schedule.date not in schedule_by_day:
            schedule_by_day[schedule.date] = []
        schedule_by_day[schedule.date].append(schedule)
    
    context = {
        'schedule_by_day': schedule_by_day,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'prev_week': start_of_week - timedelta(days=7),
        'next_week': start_of_week + timedelta(days=7),
    }
    return render(request, 'schedules/schedule_week.html', context)


@login_required
def schedule_month_view(request):
    """Расписание на месяц"""
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year and month:
        try:
            selected_date = datetime(int(year), int(month), 1).date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    
    # Первый и последний день месяца
    first_day = selected_date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1, day=1) - timedelta(days=1)
    
    if request.user.is_student():
        try:
            student_profile = request.user.student_profile
            schedules = Schedule.objects.filter(
                group=student_profile.group,
                date__range=[first_day, last_day],
                is_active=True
            ).select_related('subject', 'teacher__user', 'lesson_time').order_by('date', 'lesson_time__lesson_number')
        except StudentProfile.DoesNotExist:
            schedules = []
    elif request.user.is_teacher():
        try:
            teacher_profile = request.user.teacher_profile
            schedules = Schedule.objects.filter(
                teacher=teacher_profile,
                date__range=[first_day, last_day],
                is_active=True
            ).select_related('subject', 'group', 'lesson_time').order_by('date', 'lesson_time__lesson_number')
        except:
            schedules = []
    else:
        schedules = Schedule.objects.filter(
            date__range=[first_day, last_day],
            is_active=True
        ).select_related('subject', 'group', 'teacher__user', 'lesson_time').order_by('date', 'lesson_time__lesson_number')
    
    context = {
        'schedules': schedules,
        'selected_date': selected_date,
        'first_day': first_day,
        'last_day': last_day,
    }
    return render(request, 'schedules/schedule_month.html', context)


@login_required
def lesson_times_view(request):
    """Расписание звонков"""
    lesson_times = LessonTime.objects.all().order_by('lesson_number')
    context = {
        'lesson_times': lesson_times
    }
    return render(request, 'schedules/lesson_times.html', context)


@login_required
def notes_view(request):
    """Заметки студента"""
    if not request.user.is_student():
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    
    notes = Note.objects.filter(student=request.user).select_related(
        'schedule__subject', 'schedule__teacher__user'
    ).order_by('-created_at')
    
    context = {
        'notes': notes
    }
    return render(request, 'schedules/notes.html', context)


@login_required
def add_note_view(request, schedule_id):
    """Добавление заметки к занятию"""
    if not request.user.is_student():
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Note.objects.create(
                student=request.user,
                schedule=schedule,
                content=content
            )
            messages.success(request, 'Заметка добавлена')
            return redirect('schedules:notes')
    
    return redirect('schedules:schedule_day')


@login_required
def change_requests_view(request):
    """Список запросов на изменение (для администратора)"""
    if not (request.user.is_admin() or request.user.is_superuser):
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    
    requests = ChangeRequest.objects.select_related(
        'teacher__user', 'schedule__subject', 'schedule__group'
    ).order_by('-created_at')
    
    context = {
        'requests': requests
    }
    return render(request, 'schedules/change_requests.html', context)


@login_required
def approve_request_view(request, request_id):
    """Одобрение запроса на изменение"""
    if not (request.user.is_admin() or request.user.is_superuser):
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    
    change_request = get_object_or_404(ChangeRequest, id=request_id)
    change_request.status = 'approved'
    change_request.processed_at = timezone.now()
    change_request.processed_by = request.user
    change_request.save()
    
    messages.success(request, 'Запрос одобрен')
    return redirect('schedules:change_requests')


@login_required
def reject_request_view(request, request_id):
    """Отклонение запроса на изменение"""
    if not (request.user.is_admin() or request.user.is_superuser):
        messages.error(request, 'Доступ запрещён')
        return redirect('dashboard')
    
    change_request = get_object_or_404(ChangeRequest, id=request_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        change_request.status = 'rejected'
        change_request.processed_at = timezone.now()
        change_request.processed_by = request.user
        change_request.admin_comment = comment
        change_request.save()
        
        messages.success(request, 'Запрос отклонён')
        return redirect('schedules:change_requests')
    
    return redirect('schedules:change_requests')
