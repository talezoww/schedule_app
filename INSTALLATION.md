# 📦 Установка и настройка

## Требования

- Python 3.11 или выше
- MySQL 8.0 или выше (через XAMPP или отдельно)
- pip (менеджер пакетов Python)

## Пошаговая установка

### 1. Клонирование/Распаковка проекта

Проект находится в папке: `C:\Users\37529\Documents\lera project`

### 2. Создание виртуального окружения

```bash
# Открыть терминал в папке проекта
cd "C:\Users\37529\Documents\lera project"

# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

**Зависимости:**
- Django>=5.0.0
- mysqlclient>=2.2.0
- Pillow>=10.0.0
- python-dotenv>=1.0.0

### 4. Настройка MySQL

#### Вариант А: Через XAMPP

1. Запустите XAMPP Control Panel
2. Нажмите "Start" для модуля MySQL
3. Нажмите "Admin" для открытия phpMyAdmin
4. Перейдите на вкладку "SQL"
5. Выполните:
   ```sql
   CREATE DATABASE schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

#### Вариант Б: Через MySQL Workbench

1. Откройте MySQL Workbench
2. Подключитесь к серверу
3. Создайте новую схему (New Schema)
4. Имя: `schedule_db`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`

#### Вариант В: Через командную строку

```bash
mysql -u root -p
```

```sql
CREATE DATABASE schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 5. Настройка подключения к БД

Откройте файл `schedule_app/settings.py` и проверьте настройки:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schedule_db',
        'USER': 'root',           # Ваш пользователь MySQL
        'PASSWORD': '',           # Ваш пароль MySQL (обычно пустой для XAMPP)
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Применение миграций

```bash
# Создание файлов миграций
python manage.py makemigrations

# Применение миграций к базе данных
python manage.py migrate
```

Вы должны увидеть:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying groups.0001_initial... OK
  Applying schedules.0001_initial... OK
  ...
```

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите данные:
- **Логин**: admin (или любой другой)
- **Email**: admin@example.com
- **Пароль**: (минимум 8 символов)
- **Подтверждение пароля**: (повторите пароль)

### 8. Создание расписания звонков (обязательно!)

```bash
python manage.py shell
```

```python
from schedules.models import LessonTime
from datetime import time

# Создание расписания звонков
LessonTime.objects.create(lesson_number=1, start_time=time(8, 0), end_time=time(9, 30))
LessonTime.objects.create(lesson_number=2, start_time=time(9, 45), end_time=time(11, 15))
LessonTime.objects.create(lesson_number=3, start_time=time(11, 30), end_time=time(13, 0))
LessonTime.objects.create(lesson_number=4, start_time=time(13, 45), end_time=time(15, 15))
LessonTime.objects.create(lesson_number=5, start_time=time(15, 30), end_time=time(17, 0))

# Выход
exit()
```

### 9. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер запустится на: **http://127.0.0.1:8000/**

## 🔧 Устранение неполадок

### Ошибка: "No module named 'MySQLdb'"

```bash
pip install mysqlclient
```

Если не устанавливается на Windows, скачайте wheel-файл:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### Ошибка: "Access denied for user 'root'@'localhost'"

Проверьте пароль в `settings.py`. Для XAMPP обычно пароль пустой.

### Ошибка: "Can't connect to MySQL server"

Убедитесь, что MySQL запущен:
- В XAMPP: модуль MySQL должен быть зелёным
- В Windows Services: служба MySQL должна работать

### Порт 8000 уже используется

```bash
python manage.py runserver 8080
```

## ✅ Проверка установки

1. Откройте браузер
2. Перейдите на http://127.0.0.1:8000/
3. Вы должны увидеть страницу входа
4. Войдите с данными суперпользователя
5. Проверьте доступ к админ-панели: http://127.0.0.1:8000/admin/

## 📊 Создание тестовых данных

См. раздел "Тестовые данные" в файле [USAGE.md](USAGE.md)
