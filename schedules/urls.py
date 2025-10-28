from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('schedule/', views.schedule_day_view, name='schedule_day'),
    path('schedule/week/', views.schedule_week_view, name='schedule_week'),
    path('schedule/month/', views.schedule_month_view, name='schedule_month'),
    path('lesson-times/', views.lesson_times_view, name='lesson_times'),
    path('notes/', views.notes_view, name='notes'),
    path('notes/add/<int:schedule_id>/', views.add_note_view, name='add_note'),
    path('change-requests/', views.change_requests_view, name='change_requests'),
    path('change-requests/<int:request_id>/approve/', views.approve_request_view, name='approve_request'),
    path('change-requests/<int:request_id>/reject/', views.reject_request_view, name='reject_request'),
]
