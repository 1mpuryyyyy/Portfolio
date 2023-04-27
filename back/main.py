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


@app.route('/home')
def about():
    return render_template('about.html')


@app.route('/services', methods=['GET', 'POST'])
def services():
    form = Make_Serv()
    k = Reg_form()
    if form.upload():
        login, service, about_serv, number = k.login.data, form.service.data, form.about_serv.data, form.number.data
        if service and number: # Вань, сделай в "services.html форму для заполения описания услуги"
            print('1234321')
    return render_template('services.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    r = Reg_form()
    prov = False
    if r.Reg_submit():
        login, email, password = r.login.data, r.email.data, r.password.data
        if login and email and password and not (d.get_values(1, login)):
            d.crate_recorts_reg(login=str(login), email=str(email), password=str(password))
            prov = True
            return redirect('/'), prov  # Возвращает словарь, выбрать второй элемент(P.S. Это для Вани)
        else:
            return "Аккаунт с таким логином уже существует, попробуйте другой"

    return render_template('reg.html', title='Регистрация пользователя', form=r, proverka=prov)


@app.route('/log', methods=['GET', 'POST'])
def log():
    h = Login_form()
    check = False
    if request.method == 'POST':
        login, password = h.login.data, h.password.data
        if d.get_values(1, login) and password:
            check = True
            print(check)
            return redirect('/')
        elif login == 'Misha' and password == '12345678':
            check = True
            print(check)
            return redirect('/admin')
    return render_template('log.html', title='Вход', form=h, checking=check)


@app.route('/examples')
def examples():
    return render_template('examples.html')


@app.route('/admin')
def admin():
    return "<h1>Ваня, иди нахуй</h1>"


if __name__ == '__main__':
    app.run(debug=True)
