# 🚀 Быстрый запуск проекта

## Шаг 1: Установка зависимостей

```bash
cd "C:\Users\37529\Documents\lera project"
pip install -r requirements.txt
```

## Шаг 2: Создание базы данных MySQL

**Через XAMPP:**
1. Запустите XAMPP
2. Запустите MySQL
3. Откройте phpMyAdmin (http://localhost/phpmyadmin/)
4. Вкладка SQL → выполните:

```sql
CREATE DATABASE schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Или через командную строку:**
```bash
mysql -u root -p
```
```sql
CREATE DATABASE schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

## Шаг 3: Настройка подключения

Откройте `schedule_app/settings.py` и проверьте (строки 70-79):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schedule_db',
        'USER': 'root',
        'PASSWORD': '',  # Укажите пароль MySQL (обычно пустой для XAMPP)
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Шаг 4: Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

## Шаг 5: Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: (ваш пароль, минимум 8 символов)

## Шаг 6: Создание расписания звонков

```bash
python manage.py shell
```

Скопируйте и вставьте:
```python
from schedules.models import LessonTime
from datetime import time

LessonTime.objects.create(lesson_number=1, start_time=time(8, 0), end_time=time(9, 30))
LessonTime.objects.create(lesson_number=2, start_time=time(9, 45), end_time=time(11, 15))
LessonTime.objects.create(lesson_number=3, start_time=time(11, 30), end_time=time(13, 0))
LessonTime.objects.create(lesson_number=4, start_time=time(13, 45), end_time=time(15, 15))
LessonTime.objects.create(lesson_number=5, start_time=time(15, 30), end_time=time(17, 0))

print("Расписание звонков создано!")
exit()
```

## Шаг 7: Запуск сервера

```bash
python manage.py runserver
```

## Шаг 8: Открыть в браузере

Откройте: **http://127.0.0.1:8000/**

Войдите с учётными данными суперпользователя (admin)

## Шаг 9: Создание тестовых данных

1. Перейдите в админ-панель: http://127.0.0.1:8000/admin/
2. Создайте:
   - **Группу** (Groups → Groups → Add)
   - **Преподавателя** (создать User с role='teacher', затем Teacher Profile)
   - **Студента** (создать User с role='student', затем Student Profile)
   - **Предмет** (Groups → Subjects → Add)
   - **Расписание** (Schedules → Schedules → Add)

## 🎉 Готово!

Теперь вы можете:
- Войти как студент/преподаватель/администратор
- Просматривать расписание
- Добавлять заметки
- Управлять системой через админ-панель

## ❓ Проблемы?

**MySQL не запускается:**
- Проверьте, что порт 3306 свободен
- Перезапустите XAMPP

**Ошибка "No module named 'MySQLdb'":**
```bash
pip install mysqlclient
```

**Порт 8000 занят:**
```bash
python manage.py runserver 8080
```

Подробная документация: [README.md](README.md) | [INSTALLATION.md](INSTALLATION.md)
