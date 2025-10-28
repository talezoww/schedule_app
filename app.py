"""
Главный файл Flask приложения для системы управления расписанием
"""
from flask import Flask, redirect, url_for
from flask_login import current_user
from datetime import datetime, timedelta
import os

# Инициализация приложения
app = Flask(__name__, template_folder='templates_flask')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/schedule_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Инициализация расширений
from extensions import db, login_manager, migrate

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите в систему'

# Импорт моделей
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Импорт и регистрация blueprints
from routes import auth, admin, teacher, student, schedule

app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(teacher.bp)
app.register_blueprint(student.bp)
app.register_blueprint(schedule.bp)

@app.route('/')
def index():
    """Главная страница"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    """Панель управления в зависимости от роли"""
    from flask_login import login_required
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('teacher.dashboard'))
    else:
        return redirect(url_for('student.dashboard'))

@app.context_processor
def utility_processor():
    """Добавление утилит в контекст шаблонов"""
    return {
        'now': datetime.now(),
        'timedelta': timedelta
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
