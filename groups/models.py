from django.db import models
from accounts.models import User


class Group(models.Model):
    """Группа студентов"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название группы'
    )
    course = models.IntegerField(
        verbose_name='Курс'
    )
    faculty = models.CharField(
        max_length=200,
        verbose_name='Факультет'
    )
    head_student = models.OneToOneField(
        'accounts.StudentProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='head_of_group',
        verbose_name='Староста'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['course', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.course} курс)"
    
    def get_students_count(self):
        return self.students.count()


class Subject(models.Model):
    """Учебный предмет"""
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название предмета'
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Код предмета'
    )
    teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='subjects',
        verbose_name='Преподаватель'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    hours = models.IntegerField(
        default=0,
        verbose_name='Количество часов'
    )
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TeacherGroupAssignment(models.Model):
    """Связь преподаватель-группа-предмет"""
    
    teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.CASCADE,
        verbose_name='Преподаватель'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    semester = models.IntegerField(
        verbose_name='Семестр'
    )
    year = models.IntegerField(
        verbose_name='Учебный год'
    )
    
    class Meta:
        verbose_name = 'Назначение преподавателя'
        verbose_name_plural = 'Назначения преподавателей'
        unique_together = ['teacher', 'group', 'subject', 'semester', 'year']
    
    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.group.name} - {self.subject.name}"
