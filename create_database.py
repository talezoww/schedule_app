"""
Скрипт для создания базы данных MySQL
"""
import MySQLdb
import sys

# Попробуем разные варианты пароля
passwords = ['', 'root', 'password']

connection = None
for password in passwords:
    try:
        print(f"Пробую подключиться с паролем: '{password}' {'(пустой)' if not password else ''}")
        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password=password
        )
        print(f"Успешное подключение с паролем: '{password}' {'(пустой)' if not password else ''}")
        break
    except MySQLdb.Error:
        continue

if not connection:
    print("ОШИБКА: Не удалось подключиться ни с одним из паролей")
    print("Проверьте, что MySQL запущен в XAMPP")
    sys.exit(1)

try:
    
    cursor = connection.cursor()
    
    # Создание базы данных
    cursor.execute("CREATE DATABASE IF NOT EXISTS schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("[OK] База данных 'schedule_db' успешно создана!")
    
    # Проверка
    cursor.execute("SHOW DATABASES LIKE 'schedule_db'")
    result = cursor.fetchone()
    if result:
        print(f"[OK] Подтверждено: база данных '{result[0]}' существует")
    
    cursor.close()
    connection.close()
    print("\n[УСПЕХ] Готово! Теперь выполните миграции:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    
except MySQLdb.Error as e:
    print(f"[ОШИБКА] Ошибка при создании базы данных: {e}")
    print("\nУбедитесь что:")
    print("   1. MySQL запущен (XAMPP)")
    print("   2. Пользователь: root, Пароль: password")
    print("   3. Порт: 3306")
except ImportError:
    print("[ОШИБКА] Модуль MySQLdb не установлен")
    print("Установите: pip install mysqlclient")
