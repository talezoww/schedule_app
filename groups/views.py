from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, Subject
from accounts.models import TeacherProfile, StudentProfile


@login_required
def groups_list_view(request):
    """Список всех групп"""
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'groups/groups_list.html', context)


@login_required
def group_detail_view(request, group_id):
    """Детальная информация о группе"""
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()
    
    context = {
        'group': group,
        'students': students
    }
    return render(request, 'groups/group_detail.html', context)


@login_required
def teachers_list_view(request):
    """Список всех преподавателей"""
    teachers = TeacherProfile.objects.select_related('user').all()
    context = {
        'teachers': teachers
    }
    return render(request, 'groups/teachers_list.html', context)


@login_required
def my_groups_view(request):
    """Группы преподавателя (только для преподавателей)"""
    if not request.user.is_teacher():
        messages.error(request, 'Доступ запрещён')
        return redirect('accounts:dashboard')
    
    try:
        teacher_profile = request.user.teacher_profile
        assignments = teacher_profile.teachergroupassignment_set.select_related(
            'group', 'subject'
        ).all()
        
        context = {
            'assignments': assignments,
            'teacher': teacher_profile
        }
        return render(request, 'groups/my_groups.html', context)
    except TeacherProfile.DoesNotExist:
        messages.error(request, 'Профиль преподавателя не найден')
        return redirect('accounts:dashboard')


@login_required
def subjects_list_view(request):
    """Список всех предметов"""
    subjects = Subject.objects.select_related('teacher__user').all()
    context = {
        'subjects': subjects
    }
    return render(request, 'groups/subjects_list.html', context)
