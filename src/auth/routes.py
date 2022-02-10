"""
Blueprint for authorization
"""

from flask import Blueprint, session, render_template, request, current_app

from sql_provider import SQLProvider
from usedatabase import work_with_db


provider = SQLProvider('auth/sql')
auth_app = Blueprint('auth', __name__, template_folder='templates')


@auth_app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Function gives html for log in the system
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        flag = 0

        sql = provider.get('users.sql', login=login, password=password)

        result, schema = work_with_db(current_app.config['DB_CONFIG'], sql)
        if result:
            if result[0]['login'] == login and result[0]['password'] == password:
                session['group_name'] = result[0]['role']
                flag = 1
            else:
                flag = 0
        return render_template('result_auth.html', flag=flag, role_name=session.get('group_name'))
