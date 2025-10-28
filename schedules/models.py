from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from groups.models import Group, Subject
from accounts.models import User, TeacherProfile


class LessonTime(models.Model):
    """Расписание звонков"""
    
    lesson_number = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Номер пары'
    )
    start_time = models.TimeField(
        verbose_name='Время начала'
    )
    end_time = models.TimeField(
        verbose_name='Время окончания'
    )
    
    class Meta:
        verbose_name = 'Расписание звонков'
        verbose_name_plural = 'Расписание звонков'
        ordering = ['lesson_number']
    
    def __str__(self):
        return f"{self.lesson_number} пара: {self.start_time} - {self.end_time}"


class Schedule(models.Model):
    """Расписание занятий"""
    
    LESSON_TYPE_CHOICES = (
        ('lecture', 'Лекция'),
        ('practice', 'Практика'),
        ('lab', 'Лабораторная'),
        ('seminar', 'Семинар'),
    )
    
    WEEKDAY_CHOICES = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
    )
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        verbose_name='Преподаватель'
    )
    lesson_time = models.ForeignKey(
        LessonTime,
        on_delete=models.CASCADE,
        verbose_name='Время занятия'
    )
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        verbose_name='День недели'
    )
    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPE_CHOICES,
        default='lecture',
        verbose_name='Тип занятия'
    )
    classroom = models.CharField(
        max_length=20,
        verbose_name='Аудитория'
    )
    date = models.DateField(
        verbose_name='Дата'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Примечания'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['date', 'lesson_time__lesson_number']
    
    def __str__(self):
        return f"{self.subject.name} - {self.group.name} ({self.date})"


class Note(models.Model):
    """Заметки студента к занятию"""
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        verbose_name='Студент'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='student_notes',
        verbose_name='Занятие'
    )
    content = models.TextField(
        verbose_name='Содержание заметки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заметка {self.student.get_full_name()} - {self.schedule.subject.name}"


class ChangeRequest(models.Model):
    """Запрос на изменение расписания от преподавателя"""
    
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        verbose_name='Преподаватель'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        verbose_name='Занятие'
    )
    request_type = models.CharField(
        max_length=50,
        verbose_name='Тип запроса'
    )
    old_value = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Старое значение'
    )
    new_value = models.CharField(
        max_length=200,
        verbose_name='Новое значение'
    )
    reason = models.TextField(
        verbose_name='Причина изменения'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    admin_comment = models.TextField(
        blank=True,
        verbose_name='Комментарий администратора'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата обработки'
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_requests',
        verbose_name='Обработано'
    )
    
    class Meta:
        verbose_name = 'Запрос на изменение'
        verbose_name_plural = 'Запросы на изменение'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.request_type} ({self.get_status_display()})"
