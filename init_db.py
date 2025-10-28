"""
Скрипт инициализации базы данных
Создает таблицы и заполняет начальными данными
"""
from app import app
from extensions import db
from models import User, Group, LessonTime
from werkzeug.security import generate_password_hash
from datetime import time

def init_database():
    """Инициализация базы данных"""
    with app.app_context():
        print("Создание таблиц...")
        db.create_all()
        
        # Создание администратора
        print("\nСоздание администратора...")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@schedule.local',
                password_hash=generate_password_hash('admin'),
                first_name='Администратор',
                last_name='Системы',
                role='admin'
            )
            db.session.add(admin)
            print("✓ Администратор создан (логин: admin, пароль: admin)")
        else:
            print("✓ Администратор уже существует")
        
        # Создание расписания звонков по фото
        print("\nСоздание расписания звонков...")
        lesson_times_data = [
            # Пара 1
            (1, 1, time(8, 0), time(8, 45)),
            (1, 2, time(8, 55), time(9, 40)),
            # Пара 2
            (2, 3, time(9, 50), time(10, 35)),
            (2, 4, time(10, 45), time(11, 30)),
            # Пара 3
            (3, 5, time(11, 50), time(12, 35)),
            (3, 6, time(12, 45), time(13, 30)),
            # Пара 4
            (4, 7, time(13, 40), time(14, 25)),
            (4, 8, time(14, 35), time(15, 20)),
            # Пара 5
            (5, 9, time(15, 40), time(16, 25)),
            (5, 10, time(16, 35), time(17, 20)),
            # Пара 6
            (6, 11, time(17, 30), time(18, 15)),
            (6, 12, time(18, 25), time(19, 10)),
            # Пара 7
            (7, 13, time(19, 20), time(20, 5)),
            (7, 14, time(20, 15), time(21, 0)),
        ]
        
        for lesson_num, hour_num, start, end in lesson_times_data:
            existing = LessonTime.query.filter_by(lesson_number=lesson_num, hour_number=hour_num).first()
            if not existing:
                lesson_time = LessonTime(
                    lesson_number=lesson_num,
                    hour_number=hour_num,
                    start_time=start,
                    end_time=end
                )
                db.session.add(lesson_time)
                print(f"✓ {lesson_num} пара, {hour_num} час: {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")
        
        # Создание тестовых групп
        print("\nСоздание тестовых групп...")
        test_groups = [
            ('ИС-21', 2),
            ('ИС-31', 3),
            ('ПИ-21', 2),
            ('ПИ-31', 3),
        ]
        
        for name, course in test_groups:
            existing = Group.query.filter_by(name=name).first()
            if not existing:
                group = Group(name=name, course=course)
                db.session.add(group)
                print(f"✓ Группа {name} ({course} курс)")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("База данных успешно инициализирована!")
        print("="*50)
        print("\nДанные для входа:")
        print("  Логин: admin")
        print("  Пароль: admin")
        print("\nЗапустите приложение:")
        print("  python app.py")
        print("\nПриложение будет доступно по адресу:")
        print("  http://localhost:5000")
        print("="*50)

if __name__ == '__main__':
    init_database()
