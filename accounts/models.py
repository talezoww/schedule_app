from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя с ролями"""
    
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='Роль'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    photo = models.ImageField(
        upload_to='users/photos/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_student(self):
        return self.role == 'student'
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def is_admin(self):
        return self.role == 'admin'


class StudentProfile(models.Model):
    """Профиль студента"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Пользователь'
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Номер студенческого'
    )
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.SET_NULL,
        null=True,
        related_name='students',
        verbose_name='Группа'
    )
    enrollment_year = models.IntegerField(
        verbose_name='Год поступления'
    )
    
    class Meta:
        verbose_name = 'Профиль студента'
        verbose_name_plural = 'Профили студентов'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"


class TeacherProfile(models.Model):
    """Профиль преподавателя"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name='Пользователь'
    )
    department = models.CharField(
        max_length=200,
        verbose_name='Кафедра'
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Должность'
    )
    academic_degree = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Учёная степень'
    )
    office = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Кабинет'
    )
    
    class Meta:
        verbose_name = 'Профиль преподавателя'
        verbose_name_plural = 'Профили преподавателей'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"
