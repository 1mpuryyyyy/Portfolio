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


@app.route('/reg', meyhods=['GET', 'POST'])
def reg():
    R = Reg_form()
    if request.method == 'POST':
        name, surname, email, password = R.name.data, R.surname.data, R.email.data, R.password.data
        if name and surname and email and password:
            d.crate_recorts(name, surname, email, password)
    return render_template('reg.html', title='Регистрация', form=R)


@app.route('log')
def log():
    return render_template('log.html')


if __name__ == '__main__':
    app.run(debug=True)
