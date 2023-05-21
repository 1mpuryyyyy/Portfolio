from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, Flask, request, redirect
from formas.reg_and_log_form import Reg_form, Login_form
from formas.serv_form import Make_Serv
from sends_emails import send_email, send_emal_to_user
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
def home():
    return render_template('home.html', title='home')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route('/home')
def about():
    return render_template('about.html', title='about', current_user=current_user)


def allowed_type(filename, types):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in types


@app.route('/services', methods=['GET', 'POST'])
def services():
    if current_user.is_authenticated:
        form = Make_Serv()
        if request.method == 'POST':
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(
                User.id == current_user.id).first()  # ищет нужного пользователя через query
            name, surname, service, about_serv, number = current_user.name, current_user.surname, form.service.data, \
                                                         form.about_serv.data, form.number.data
            files = request.files.getlist("photo[]")  # Забирает фотки из формы
            if files:
                f_count = 0
                for file in files:
                    if allowed_type(file.filename, ['png', 'jpg', 'docx', 'doc', 'txt']):
                        filename = f"{current_user.id}_{user.id_serv}_{f_count}.{file.filename.rsplit('.', 1)[1].lower()}"  # название файла
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        f_count += 1
            user.id_serv += 1
            db_sess.commit()
            if service and number:
                send_email(f"{name} {surname}, хочет заказать у вас услугу: {service}, Описание:"
                           f" {about_serv}. Номер телефона: {number} Номер заказа: {user.id_serv - 1}")
                send_emal_to_user(
                    f"Над заказом, {service}, была начата работа, наши спецалисты в скром времени свяжутся с вами и уточнят подробности",
                    current_user.email, 0)

    else:
        return redirect('/reg')

    return render_template('services.html', name_user=current_user.name, form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
        h = Reg_form()
        db_sess = db_session.create_session()
        if request.method == 'POST':
            name, surname, email, password = h.name.data, h.surname.data, h.email.data, h.password.data
            if name and email and password:
                user = db_sess.query(User).filter(User.email == email).first()
                if not (user and check_password_hash(user.hashed_password, password)):
                    user = User()
                    user.name = name
                    user.email = email
                    user.surname = surname
                    user.hashed_password = generate_password_hash(password)  # Хэширует пароль
                    db_sess.add(user)
                    db_sess.commit()
                    login_user(user)
                    send_emal_to_user(f"{current_user.name} {current_user.surnmae}, ваш аккаунт успешно зарегистирован", current_user.email, 0)
                    return redirect('/home')
                else:
                    return redirect('/log')
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
                send_emal_to_user(f"{current_user.name} {current_user.surnmae}, успешный вход в аккаунт", current_user.email, 0)
                return redirect('/home')
            else:
                return redirect('/reg')
    return render_template('log.html', title='Вход')


@app.route('/examples')
def examples():
    return render_template('examples.html')


if __name__ == '__main__':
    db_session.global_init('database.db')
    app.run(debug=True)
