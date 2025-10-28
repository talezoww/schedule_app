from django.contrib import admin
from .models import Group, Subject, TeacherGroupAssignment


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'faculty', 'head_student', 'get_students_count')
    list_filter = ('course', 'faculty')
    search_fields = ('name', 'faculty')
    
    def get_students_count(self, obj):
        return obj.get_students_count()
    get_students_count.short_description = 'Количество студентов'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'hours')
    list_filter = ('teacher',)
    search_fields = ('name', 'code')


@admin.register(TeacherGroupAssignment)
class TeacherGroupAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'group', 'subject', 'semester', 'year')
    list_filter = ('semester', 'year', 'group')
    search_fields = ('teacher__user__last_name', 'group__name', 'subject__name')
