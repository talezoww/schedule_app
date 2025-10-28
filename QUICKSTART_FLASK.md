# 🚀 Быстрый старт - Flask версия

## Минимальная установка за 5 минут

### 1. Клонирование репозитория
```bash
git clone https://github.com/talezoww/schedule_app.git
cd schedule_app
```

### 2. Установка зависимостей
```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/Mac)
# source venv/bin/activate

# Установка пакетов
pip install -r requirements_flask.txt
```

### 3. Настройка MySQL
```bash
# Войдите в MySQL
mysql -u root -p

# Создайте базу данных
CREATE DATABASE schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 4. Создание .env файла
Создайте файл `.env` в корне проекта:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:your_password@localhost/schedule_db
```

### 5. Инициализация БД
```bash
python init_db.py
```

### 6. Запуск
```bash
python app.py
```

Откройте браузер: **http://localhost:5000**

### 7. Вход
- Логин: `admin`
- Пароль: `admin`

## ✅ Что создано

- ✅ 9 таблиц БД
- ✅ Администратор (admin/admin)
- ✅ Расписание звонков (7 пар)
- ✅ Тестовые группы (ИС-21, ИС-31, ПИ-21, ПИ-31)

## 📝 Следующие шаги

1. Измените пароль администратора
2. Создайте предметы через админ-панель
3. Пользователи регистрируются → Вы подтверждаете
4. Преподаватели добавляют занятия
5. Студенты просматривают расписание

## ❗ Проблемы?

См. полную инструкцию: [INSTALLATION_FLASK.md](INSTALLATION_FLASK.md)
