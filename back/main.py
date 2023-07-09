from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, Flask, request, redirect, url_for
from formas.reg_and_log_form import Reg_form, Login_form
from formas.serv_form import *
from sends_emails import *
from data import db_session
from data.user import User
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'sxcc1cf4c152bhfbu2cs51cd14;'
app.config['UPLOAD_FOLDER'] = 'uploads'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "Cмотреть данную страницу/делать данное действие можно " \
                              "только авторизованным пользователям"


@login_manager.user_loader
def load_user(user_id: int):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


@app.route('/')
def about():
    return render_template('pattern.html', title='about', current_user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))


def allowed_type(filename, types):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in types


@app.route('/serv', methods=['GET', 'POST'])
def serv():
    servi = ['Написание БД', 'Верстка сайта', 'Монтаж видео', 'Видеосъемка']
    if current_user.is_authenticated:
        form = Make_Serv()
        if request.method == 'POST':
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(
                User.id == current_user.id).first()  # ищет нужного пользователя через query
            name, surname, about_serv, number = current_user.name, current_user.surname, form.about_serv.data, form.number.data
            files = request.files.getlist("photo[]")  # Забирает фотки из формы [] - для множественного набора
            if files:
                f_count = 0
                for file in files:
                    if allowed_type(file.filename, ['png', 'jpg', 'docx', 'doc', 'txt']):
                        filename = f"{current_user.id}_{user.id_serv}_{f_count}.{file.filename.rsplit('.', 1)[1].lower()}"  # название файла
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        f_count += 1
            user.id_serv += 1
            db_sess.commit()
            if about_serv and number:
                send_email(
                    f"{name} {surname}, сделал заказ."
                    f" Описание:{about_serv}."
                    f" Номер телефона: {number}."
                    f" Номер заказа: {user.id_serv - 1}.")
                send_email_to_user(
                    f"Над вашим заказом, была начата работа, наши спецалисты в скором времени свяжутся с вами и уточнят подробности",
                    current_user.email, 1)

    else:
        return redirect(url_for('reg'))

    return render_template('serv.html', name_user=current_user.name, form=form, elems=servi)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    h = Reg_form()
    db_sess = db_session.create_session()
    if request.method == 'POST':
        name, surname, email, password = h.name.data, h.surname.data, h.email.data, h.password.data
        if name and email and password:
            user = db_sess.query(User).filter(User.email == email).first()
            if not user:
                user = User()
                user.name = name
                user.email = email
                user.surname = surname
                user.hashed_password = generate_password_hash(password)  # Хэширует пароль
                db_sess.add(user)
                db_sess.commit()
                login_user(user)
                send_email_to_user(f"{current_user.name} {current_user.surname}, ваш аккаунт успешно зарегистирован",
                                   current_user.email, 0)
                return redirect('/')
            else:
                return redirect(url_for('log'))
    return render_template('reg.html', title='Регистрация пользователя', form=h)


@app.route('/log', methods=['GET', 'POST'])
def log():
    f = Login_form()
    db_sess = db_session.create_session()
    if request.method == 'POST':
        email, password = f.email.data, f.password.data
        if email and password:
            user = db_sess.query(User).filter(User.email == email).first()
            if user and check_password_hash(user.hashed_password, password):
                login_user(user)
                return redirect(url_for('about'))
            else:
                return redirect(url_for('reg'))
    return render_template('log.html', title='Вход')


@app.route('/examples')
def examples():
    return render_template('examples.html')


if __name__ == '__main__':
    db_session.global_init('database.db')
    app.run(debug=True)
