from flask import render_template, Flask, request, redirect
from formas.reg_and_log_form import Reg_form, Login_form
from formas.serv_form import Make_Serv
from db import Database

d = Database('database.db')
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
def home():
    return render_template('home.html', title='home')


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/services', methods=['GET', 'POST'])
def services():
    form = Make_Serv()
    # if form.upload():
    #     login, service, about_serv, number = d.get_values()[-1], form.service.data, form.about_serv.data, form.number.data
    #     if service and number:  # Вань, сделай в "services.html" форму для заполения описания услуги"
    #         send_email(f"{login}, хочет заказать у вас услугу: {service}, Описание: {number}")

    return render_template('services.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    r = Reg_form()
    if request.method == 'POST':
        login, email, password = r.login.data, r.email.data, r.password.data
        if login and email and password and not (d.get_values(login)):
            d.crate_recorts_reg(login=str(login), email=str(email), password=str(password))
            return redirect('/home')
        else:
            return redirect('/log')

    return render_template('reg.html', title='Регистрация пользователя', form=r)


@app.route('/log', methods=['GET', 'POST'])
def log():
    h = Login_form()
    if request.method == 'POST':
        login, password = h.login.data, h.password.data
        if d.get_values(login) and password:
            return redirect('/home')
    return render_template('log.html', title='Вход', form=h)


@app.route('/examples')
def examples():
    return render_template('examples.html')


if __name__ == '__main__':
    app.run(debug=True)
