"""
Скрипт для начальной настройки: пароль админа и расписание звонков
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schedule_app.settings')
django.setup()

from django.contrib.auth import get_user_model
from schedules.models import LessonTime
from datetime import time

User = get_user_model()

print("[1/2] Установка пароля для администратора...")
try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin')  # Пароль: admin
    admin.role = 'admin'
    admin.save()
    print("[OK] Пароль установлен (логин: admin, пароль: admin)")
except User.DoesNotExist:
    print("[ОШИБКА] Пользователь admin не найден")

print("\n[2/2] Создание расписания звонков...")
lesson_times = [
    (1, time(8, 0), time(9, 30)),
    (2, time(9, 45), time(11, 15)),
    (3, time(11, 30), time(13, 0)),
    (4, time(13, 45), time(15, 15)),
    (5, time(15, 30), time(17, 0)),
    (6, time(17, 15), time(18, 45)),
]

for lesson_number, start_time, end_time in lesson_times:
    LessonTime.objects.get_or_create(
        lesson_number=lesson_number,
        defaults={'start_time': start_time, 'end_time': end_time}
    )
    print(f"[OK] {lesson_number} пара: {start_time} - {end_time}")

print("\n[УСПЕХ] Начальная настройка завершена!")
print("\nВы можете:")
print("1. Запустить сервер: python manage.py runserver")
print("2. Войти в систему:")
print("   - Логин: admin")
print("   - Пароль: admin")
print("3. Админ-панель: http://127.0.0.1:8000/admin/")
