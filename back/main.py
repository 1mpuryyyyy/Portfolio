from flask import render_template, Flask, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.user import User
from formas.reg_and_log_form import Reg_form, Login_form
from formas.serv_form import Make_Serv
from sends_emails import send_email

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'sxcc1cf4c152bhfbu2cs51cd14;'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "Cмотреть данную страницу/делать данное действие можно " \
                              "только авторизованным пользователям"


@login_manager.user_loader
def load_user(user_id: int):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/')
def home():
    return render_template('home.html', title='home')


@app.route('/home')
def about():
    return render_template('about.html', title='about', current_user=current_user)


@app.route('/services', methods=['GET', 'POST'])
@login_required
def services():
    form = Make_Serv()
    if form.upload():
        name, service, about_serv, number = current_user.name, form.service.data, form.about_serv.data, form.number.data
        if service and number:
            send_email(
                f"{name}, хочет заказать у вас услугу: {service}, Описание: {about_serv}. Номер телефона: {number}")

    return render_template('services.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    h = Reg_form()
    db_sess = db_session.create_session()
    if request.method == 'POST':
        name, email, password = h.name.data, h.email.data, h.password.data
        if name and email and password:
            user = User()
            user.name = name
            user.email = email
            user.hashed_password = generate_password_hash(password)  # Хэширует пароль
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/home')
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
                return redirect('/home')
    return render_template('log.html', title='Вход')


@app.route('/examples')
def examples():
    return render_template('examples.html')


if __name__ == '__main__':
    db_session.global_init('database.db')
    app.run(debug=True)
