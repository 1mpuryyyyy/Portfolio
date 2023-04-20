from flask import render_template, Flask

app = Flask(__name__, template_folder='../templates')
app.config['secret_key'] = 'secret_key'


@app.route('/')
def home():
    return render_template('home.html', title='home')


if __name__ == '__main__':
    app.run(debug=True)
