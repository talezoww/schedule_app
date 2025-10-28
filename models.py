"""
Модели базы данных для системы управления расписанием
9 таблиц: User, PendingUser, Group, Subject, Teacher, Student, Schedule, LessonTime, Note
"""
from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """Таблица 1: Пользователи системы"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # admin, teacher, student
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    teacher = db.relationship('Teacher', backref='user', uselist=False, cascade='all, delete-orphan')
    student = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    notes = db.relationship('Note', backref='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class PendingUser(db.Model):
    """Таблица 2: Ожидающие подтверждения пользователи"""
    __tablename__ = 'pending_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    requested_role = db.Column(db.String(20), nullable=False)  # teacher или student
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)  # Для студентов
    course = db.Column(db.Integer, nullable=True)  # Для студентов
    department = db.Column(db.String(200), nullable=True)  # Для преподавателей
    position = db.Column(db.String(100), nullable=True)  # Для преподавателей
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    group = db.relationship('Group', backref='pending_students')
    
    def __repr__(self):
        return f'<PendingUser {self.username}>'


class Group(db.Model):
    """Таблица 3: Учебные группы"""
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    course = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    students = db.relationship('Student', backref='group', cascade='all, delete-orphan')
    schedules = db.relationship('Schedule', backref='group', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Group {self.name}>'
    
    def get_students_count(self):
        return len(self.students)


class Subject(db.Model):
    """Таблица 4: Учебные предметы"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    hours = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    schedules = db.relationship('Schedule', backref='subject', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'


class Teacher(db.Model):
    """Таблица 5: Преподаватели"""
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    department = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    academic_degree = db.Column(db.String(100))
    office = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    schedules = db.relationship('Schedule', backref='teacher', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Teacher {self.user.get_full_name()}>'


class Student(db.Model):
    """Таблица 6: Студенты"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Student {self.user.get_full_name()}>'


class LessonTime(db.Model):
    """Таблица 7: Расписание звонков"""
    __tablename__ = 'lesson_times'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_number = db.Column(db.Integer, unique=True, nullable=False, index=True)
    hour_number = db.Column(db.Integer, nullable=False)  # Номер часа (1-14)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # Связи
    schedules = db.relationship('Schedule', backref='lesson_time', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<LessonTime {self.lesson_number}: {self.start_time}-{self.end_time}>'
    
    def get_time_range(self):
        return f'{self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")}'


class Schedule(db.Model):
    """Таблица 8: Расписание занятий"""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    lesson_time_id = db.Column(db.Integer, db.ForeignKey('lesson_times.id'), nullable=False)
    weekday = db.Column(db.Integer, nullable=False)  # 1-6 (Пн-Сб)
    lesson_type = db.Column(db.String(20), default='lecture')  # lecture, practice, lab, seminar
    classroom = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    student_notes = db.relationship('Note', backref='schedule', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Schedule {self.subject.name} - {self.group.name}>'
    
    def get_weekday_name(self):
        weekdays = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 
                   4: 'Четверг', 5: 'Пятница', 6: 'Суббота'}
        return weekdays.get(self.weekday, '')
    
    def get_lesson_type_display(self):
        types = {'lecture': 'Лекция', 'practice': 'Практика', 
                'lab': 'Лабораторная', 'seminar': 'Семинар'}
        return types.get(self.lesson_type, self.lesson_type)


class Note(db.Model):
    """Таблица 9: Заметки студентов к занятиям"""
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Note by {self.user.username}>'
