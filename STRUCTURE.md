# 📁 Структура проекта

## Обзор директорий

```
schedule_app/
│
├── manage.py                          # Управление Django проектом
├── requirements.txt                   # Python зависимости
├── README.md                          # Главная документация
├── INSTALLATION.md                    # Инструкция по установке
├── USAGE.md                           # Руководство пользователя
├── STRUCTURE.md                       # Этот файл
│
├── schedule_app/                      # Главное приложение Django
│   ├── __init__.py
│   ├── settings.py                    # Настройки проекта
│   ├── urls.py                        # Главные URL маршруты
│   ├── wsgi.py                        # WSGI конфигурация
│   └── asgi.py                        # ASGI конфигурация
│
├── accounts/                          # Приложение авторизации
│   ├── __init__.py
│   ├── admin.py                       # Настройки админ-панели
│   ├── apps.py                        # Конфигурация приложения
│   ├── models.py                      # Модели User, StudentProfile, TeacherProfile
│   ├── views.py                       # Представления (вход, регистрация, профиль)
│   ├── forms.py                       # Формы
│   ├── urls.py                        # URL маршруты
│   └── templates/accounts/            # Шаблоны
│       ├── login.html
│       ├── register.html
│       └── profile.html
│
├── groups/                            # Приложение групп и предметов
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # Модели Group, Subject, TeacherGroupAssignment
│   ├── views.py                       # Представления
│   ├── urls.py
│   └── templates/groups/
│       ├── groups_list.html           # Список групп
│       ├── group_detail.html          # Детали группы
│       ├── teachers_list.html         # Список преподавателей
│       ├── my_groups.html             # Группы преподавателя
│       └── subjects_list.html         # Список предметов
│
├── schedules/                         # Приложение расписания
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # Модели Schedule, Note, LessonTime, ChangeRequest
│   ├── views.py                       # Представления
│   ├── urls.py
│   └── templates/schedules/
│       ├── schedule_day.html          # Расписание на день
│       ├── schedule_week.html         # Расписание на неделю
│       ├── schedule_month.html        # Расписание на месяц
│       ├── lesson_times.html          # Расписание звонков
│       ├── notes.html                 # Заметки студента
│       └── change_requests.html       # Запросы на изменение
│
├── templates/                         # Общие шаблоны
│   ├── base.html                      # Базовый шаблон с sidebar
│   ├── dashboard_student.html         # Панель студента
│   ├── dashboard_teacher.html         # Панель преподавателя
│   └── dashboard_admin.html           # Панель администратора
│
├── static/                            # Статические файлы
│   ├── css/
│   │   └── style.css                  # Основные стили
│   └── js/
│       └── main.js                    # JavaScript функции
│
├── media/                             # Загружаемые файлы (создаётся автоматически)
│   └── users/
│       └── photos/                    # Фото пользователей
│
└── db/                                # SQL скрипты
    └── init.sql                       # Инициализация и примеры запросов
```

## Описание моделей

### accounts.models

**User** (расширенный AbstractUser)
- Поля: username, email, first_name, last_name, role, phone, photo
- Методы: is_student(), is_teacher(), is_admin()

**StudentProfile**
- Связь: OneToOne с User
- Поля: student_id, group (FK), enrollment_year

**TeacherProfile**
- Связь: OneToOne с User
- Поля: department, position, academic_degree, office

### groups.models

**Group**
- Поля: name, course, faculty, head_student (FK), created_at
- Методы: get_students_count()

**Subject**
- Поля: name, code, teacher (FK), description, hours

**TeacherGroupAssignment**
- Поля: teacher (FK), group (FK), subject (FK), semester, year
- Связывает преподавателя с группой и предметом

### schedules.models

**LessonTime**
- Поля: lesson_number, start_time, end_time
- Расписание звонков

**Schedule**
- Поля: subject (FK), group (FK), teacher (FK), lesson_time (FK)
- Поля: weekday, date, lesson_type, classroom, is_active, notes

**Note**
- Поля: student (FK), schedule (FK), content
- Заметки студентов к занятиям

**ChangeRequest**
- Поля: teacher (FK), schedule (FK), request_type, old_value, new_value
- Поля: reason, status, admin_comment, processed_by (FK)
- Запросы на изменение расписания

## URL маршруты

### Главные URL (schedule_app/urls.py)
```python
/                           → redirect to /dashboard/
/admin/                     → Django Admin
/                           → include accounts.urls
/                           → include schedules.urls
/                           → include groups.urls
```

### accounts.urls
```python
/login/                     → LoginView
/register/                  → RegisterView
/logout/                    → logout_view
/profile/                   → profile_view
/dashboard/                 → dashboard_view
```

### schedules.urls
```python
/schedule/                  → schedule_day_view
/schedule/week/             → schedule_week_view
/schedule/month/            → schedule_month_view
/lesson-times/              → lesson_times_view
/notes/                     → notes_view
/notes/add/<int:id>/        → add_note_view
/change-requests/           → change_requests_view
/change-requests/<int:id>/approve/  → approve_request_view
/change-requests/<int:id>/reject/   → reject_request_view
```

### groups.urls
```python
/groups/                    → groups_list_view
/groups/<int:id>/           → group_detail_view
/teachers/                  → teachers_list_view
/my-groups/                 → my_groups_view
/subjects/                  → subjects_list_view
```

## Настройки (settings.py)

### Важные параметры

**SECRET_KEY** - секретный ключ Django (изменить для продакшена!)

**DEBUG** - режим отладки (False для продакшена)

**ALLOWED_HOSTS** - разрешённые хосты

**DATABASES** - настройки MySQL
```python
'ENGINE': 'django.db.backends.mysql'
'NAME': 'schedule_db'
'USER': 'root'
'PASSWORD': ''
'HOST': 'localhost'
'PORT': '3306'
```

**AUTH_USER_MODEL** - кастомная модель пользователя
```python
AUTH_USER_MODEL = 'accounts.User'
```

**STATIC_URL** - URL для статических файлов
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**MEDIA_URL** - URL для загружаемых файлов
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Статические файлы

### CSS (static/css/style.css)
- Стили для sidebar
- Адаптивный дизайн
- Стили для карточек и таблиц
- Анимации

### JavaScript (static/js/main.js)
- Toggle sidebar
- Автоскрытие alerts
- Подтверждение удаления
- Активная навигация
- Инициализация Bootstrap компонентов

## Шаблоны

### base.html
Базовый шаблон со структурой:
- Sidebar с навигацией (для авторизованных)
- Основной контент
- Bootstrap 5 подключение
- Статические файлы

### Дашборды
- **dashboard_student.html** - карточки с основными функциями студента
- **dashboard_teacher.html** - карточки для преподавателя
- **dashboard_admin.html** - панель администратора

### Блоки в шаблонах
```django
{% block title %}          # Заголовок страницы
{% block extra_css %}      # Дополнительные стили
{% block content %}        # Основной контент
{% block extra_js %}       # Дополнительный JavaScript
```

## База данных

### Таблицы (автоматически создаются Django)

- accounts_user
- accounts_studentprofile
- accounts_teacherprofile
- groups_group
- groups_subject
- groups_teachergroupassignment
- schedules_lessontime
- schedules_schedule
- schedules_note
- schedules_changerequest

### Индексы и связи

Django ORM автоматически создаёт:
- Primary keys (id)
- Foreign keys с индексами
- Unique constraints
- Индексы для часто запрашиваемых полей

## Расширение проекта

### Добавление нового приложения

```bash
python manage.py startapp app_name
```

1. Добавить в INSTALLED_APPS (settings.py)
2. Создать models.py
3. Создать views.py
4. Создать urls.py
5. Подключить в главный urls.py
6. Создать templates/app_name/
7. Выполнить миграции

### Добавление новой модели

1. Описать в models.py
2. Зарегистрировать в admin.py
3. Создать миграции: `python manage.py makemigrations`
4. Применить: `python manage.py migrate`

### Добавление нового URL

1. Создать view функцию/класс
2. Добавить path в urls.py
3. Создать шаблон
