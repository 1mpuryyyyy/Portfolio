from flask import render_template, Flask, request
from formas.reg_and_log_form import Reg_form, Login_form
from db import Database

d = Database
app = Flask(__name__, template_folder='../templates')
app.config['secret_key'] = 'secret_key'


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
    if request.method == 'POST':
        name, surname, email, password = r.name.data, r.surname.data, r.email.data, r.password.data
        if name and surname and email and password:
            d.crate_recorts_reg(name, surname, email, password)
    return render_template('reg.html', title='Регистрация пользователя', form=r)


@app.route('/log', methods=['GET', 'POST'])
def log():
    h = Login_form()
    if request.method == 'POST':
        email, password = h.email.data, h.password.data
        if email and password:
            d.creating_tables_log(email, password)
    return render_template('log.html', title='Вход', form=h)


@app.route('/examples')
def examples():
    return render_template('examples.html')


if __name__ == '__main__':
    app.run(debug=True)
