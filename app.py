import os
from flask import Flask, render_template, request, redirect
from  werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-later')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construct_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def get_id(self):
        return str(self.id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('register.html', error='Заполни все поля')

        if len(password) < 8:
            return render_template('register.html', error='Пароль должен содержать минимум 8 символов')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template('register.html', error='Эта почта уже зарегистрирована')

        password_hash = generate_password_hash(password)

        new_user = User(
            email=email,
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect('/')

    return render_template('register.html')
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = None  # Здесь будем хранить ответ для пользователя
    
    if request.method == 'POST':
        # Получаем то, что пользователь написал в поле с именем "description"
        user_description = request.form.get('description', '')
        
        # ЗАГЛУШКА: вместо реального 3D-генератора просто возвращаем текст
        # Позже мы заменим эту строку на вызов настоящего API
        if user_description:
            result_text = f"Вы описали: «{user_description}». (Здесь скоро появится 3D-модель!)"
        else:
            result_text = "Вы ничего не написали. Попробуйте ещё раз."
    
    # Передаём результат в HTML-шаблон, чтобы страница его показала
    return render_template('index.html', result=result_text, user=current_user)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Эта часть нужна для локального запуска, Render использует gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
