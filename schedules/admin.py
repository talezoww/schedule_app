from django.contrib import admin
from .models import LessonTime, Schedule, Note, ChangeRequest


@admin.register(LessonTime)
class LessonTimeAdmin(admin.ModelAdmin):
    list_display = ('lesson_number', 'start_time', 'end_time')
    ordering = ('lesson_number',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'group', 'teacher', 'date', 'lesson_time', 'classroom', 'is_active')
    list_filter = ('date', 'weekday', 'lesson_type', 'is_active', 'group')
    search_fields = ('subject__name', 'group__name', 'teacher__user__last_name', 'classroom')
    date_hierarchy = 'date'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('student', 'schedule', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('student__username', 'content', 'schedule__subject__name')


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'schedule', 'request_type', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'request_type')
    search_fields = ('teacher__user__last_name', 'reason')
    readonly_fields = ('created_at', 'processed_at')
