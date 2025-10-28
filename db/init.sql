-- SQL скрипт для инициализации базы данных MySQL
-- Система управления расписанием

-- Создание базы данных
CREATE DATABASE IF NOT EXISTS schedule_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE schedule_db;

-- Примечание: Django автоматически создаст все таблицы при выполнении миграций
-- Этот скрипт содержит полезные запросы для работы с БД

-- Проверка существующих таблиц
SHOW TABLES;

-- Создание пользователя для приложения (опционально)
-- CREATE USER 'schedule_user'@'localhost' IDENTIFIED BY 'password';
-- GRANT ALL PRIVILEGES ON schedule_db.* TO 'schedule_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Примеры запросов для добавления тестовых данных после миграции

-- Добавление расписания звонков (после создания таблиц Django)
/*
INSERT INTO schedules_lessontime (lesson_number, start_time, end_time) VALUES
(1, '08:00:00', '09:30:00'),
(2, '09:45:00', '11:15:00'),
(3, '11:30:00', '13:00:00'),
(4, '13:45:00', '15:15:00'),
(5, '15:30:00', '17:00:00'),
(6, '17:15:00', '18:45:00');
*/

-- Запрос для просмотра всех пользователей по ролям
/*
SELECT 
    u.id,
    u.username,
    CONCAT(u.first_name, ' ', u.last_name) as full_name,
    u.email,
    u.role,
    u.date_joined
FROM accounts_user u
ORDER BY u.role, u.last_name;
*/

-- Запрос для просмотра расписания конкретной группы
/*
SELECT 
    s.date,
    s.weekday,
    lt.lesson_number,
    lt.start_time,
    lt.end_time,
    subj.name as subject_name,
    s.lesson_type,
    s.classroom,
    CONCAT(t.first_name, ' ', t.last_name) as teacher_name
FROM schedules_schedule s
JOIN schedules_lessontime lt ON s.lesson_time_id = lt.id
JOIN groups_subject subj ON s.subject_id = subj.id
JOIN groups_group g ON s.group_id = g.id
JOIN accounts_teacherprofile tp ON s.teacher_id = tp.id
JOIN accounts_user t ON tp.user_id = t.id
WHERE g.name = 'ПИ-21'
ORDER BY s.date, lt.lesson_number;
*/

-- Запрос для подсчета студентов по группам
/*
SELECT 
    g.name as group_name,
    g.course,
    g.faculty,
    COUNT(sp.id) as students_count
FROM groups_group g
LEFT JOIN accounts_studentprofile sp ON sp.group_id = g.id
GROUP BY g.id, g.name, g.course, g.faculty
ORDER BY g.course, g.name;
*/

-- Запрос для просмотра нагрузки преподавателей
/*
SELECT 
    CONCAT(u.first_name, ' ', u.last_name) as teacher_name,
    tp.department,
    COUNT(DISTINCT s.id) as lessons_count,
    COUNT(DISTINCT s.group_id) as groups_count
FROM accounts_teacherprofile tp
JOIN accounts_user u ON tp.user_id = u.id
LEFT JOIN schedules_schedule s ON s.teacher_id = tp.id
GROUP BY tp.id, u.first_name, u.last_name, tp.department
ORDER BY lessons_count DESC;
*/

-- Запрос для просмотра запросов на изменение расписания
/*
SELECT 
    cr.id,
    CONCAT(t.first_name, ' ', t.last_name) as teacher_name,
    subj.name as subject_name,
    g.name as group_name,
    cr.request_type,
    cr.old_value,
    cr.new_value,
    cr.reason,
    cr.status,
    cr.created_at
FROM schedules_changerequest cr
JOIN accounts_teacherprofile tp ON cr.teacher_id = tp.id
JOIN accounts_user t ON tp.user_id = t.id
JOIN schedules_schedule s ON cr.schedule_id = s.id
JOIN groups_subject subj ON s.subject_id = subj.id
JOIN groups_group g ON s.group_id = g.id
WHERE cr.status = 'pending'
ORDER BY cr.created_at DESC;
*/

-- Очистка тестовых данных (использовать осторожно!)
/*
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE schedules_schedule;
TRUNCATE TABLE schedules_note;
TRUNCATE TABLE schedules_changerequest;
TRUNCATE TABLE accounts_studentprofile;
TRUNCATE TABLE accounts_teacherprofile;
TRUNCATE TABLE groups_group;
TRUNCATE TABLE groups_subject;
SET FOREIGN_KEY_CHECKS = 1;
*/

-- Резервное копирование базы данных (выполнить в командной строке)
-- mysqldump -u root -p schedule_db > backup.sql

-- Восстановление из резервной копии (выполнить в командной строке)
-- mysql -u root -p schedule_db < backup.sql
