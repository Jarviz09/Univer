import json
import access

from flask import Flask, render_template, session

from requests.routes import request_app
from auth.routes import auth_app
from basket.routes import basket_app

app = Flask(__name__)

app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['SECRET_KEY'] = 'my super secret key'
app.config['DB_CONFIG'] = json.load(open('configs/dbconfig.json'))


app.register_blueprint(request_app, url_prefix='/requests')  # /user/get, /user/* -> user_app
app.register_blueprint(auth_app, url_prefix='/auth')  # /user/get, /user/* -> user_app
app.register_blueprint(basket_app, url_prefix='/basket')  # /user/get, /user/* -> user_app


@app.route('/exit')
def exit():
    session.clear()
    return render_template('exit.html')


@app.route('/')
def menu():
    func = {'group_permission_validation': access.group_permission_validation}
    return render_template('main_menu.html', func=func)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

