"""
Скрипт для пересоздания базы данных MySQL
"""
import MySQLdb

try:
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        password='password'
    )
    
    cursor = connection.cursor()
    
    print("[1/3] Удаление старой базы данных...")
    cursor.execute("DROP DATABASE IF EXISTS schedule_db")
    print("[OK] Старая база данных удалена")
    
    print("[2/3] Создание новой базы данных...")
    cursor.execute("CREATE DATABASE schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("[OK] База данных 'schedule_db' создана")
    
    print("[3/3] Проверка...")
    cursor.execute("SHOW DATABASES LIKE 'schedule_db'")
    result = cursor.fetchone()
    if result:
        print(f"[OK] Подтверждено: база данных '{result[0]}' существует")
    
    cursor.close()
    connection.close()
    
    print("\n[УСПЕХ] База данных готова!")
    print("\nТеперь выполните:")
    print("   python manage.py migrate")
    
except MySQLdb.Error as e:
    print(f"[ОШИБКА] {e}")
    print("Проверьте, что MySQL запущен")
