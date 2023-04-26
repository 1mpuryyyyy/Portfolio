from flask import render_template, Flask, request
from formas.reg_and_log_form import Reg_form, Login_form
from db import Database

d = Database('database.db')
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
def home():
    return render_template('home.html', title='home')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    r = Reg_form()
    if r.Reg_submit():
        name, surname, email, password = r.name.data, r.surname.data, r.email.data, r.password.data
        if name and surname and email and password:
            print('1323')
            d.crate_recorts_reg(name=str(name), surname=str(surname), email=str(email), password=str(password))
    return render_template('reg.html', title='Регистрация пользователя', form=r)


@app.route('/admin')
def admin():
    return render_template('')


@app.route('/log', methods=['GET', 'POST'])
def log():
    h = Login_form()
    if h.log_sub():
        email, password = h.email.data, h.password.data
        pass



    return render_template('log.html', title='Вход', form=h)


@app.route('/examples')
def examples():
    return render_template('examples.html')


if __name__ == '__main__':
    app.run(debug=True)
