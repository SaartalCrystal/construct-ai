import os
from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template('index.html', result=result_text)

if __name__ == '__main__':
    # Эта часть нужна для локального запуска, Render использует gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
