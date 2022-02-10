"""
Blueprint which shows implemented requests
"""

from flask import Blueprint, render_template, request, current_app

from access import group_permission_decorator
from sql_provider import SQLProvider
from usedatabase import work_with_db


request_app = Blueprint('requests', __name__, template_folder='templates')

provider = SQLProvider('requests/sql')


@request_app.route('/')
@group_permission_decorator
def request_menu():
    return render_template('requests.html')


@request_app.route('/first', methods=['GET', 'POST'])
@group_permission_decorator
def first():
    """
    Function gives result of the first SQL request
    :return:
    """
    if request.method == 'GET':
        return render_template('one_request.html')
    else:
        name = request.form['name']
        sql = provider.get('request_one.sql', name=name)
        db_config = current_app.config['DB_CONFIG']
        result, schema = work_with_db(db_config, sql)
        context = {'schema': schema, 'data': result}
        if result:
            return render_template('request_one_table.html', context=context)
        else:
            return render_template('result_is_empty.html')


@request_app.route('/second', methods=['GET', 'POST'])
@group_permission_decorator
def second():
    """
    Function gives result of the second SQL request
    :return:
    """
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        SQL = provider.get('suppliers.sql')
        result2, schema2 = work_with_db(db_config, SQL)
        return render_template('two_request.html', result=result2)

    name = request.form['name']
    year = request.form['year']

    print(name)
    print(year)

    sql = provider.get('request_two.sql', name=name, year=year)

    result1, schema1 = work_with_db(db_config, sql)

    context = {'schema': schema1, 'data': result1}

    print(context)

    if result1:
        return render_template('request_two_table.html', context=context)
    else:
        return render_template('result_is_empty.html')


@request_app.route('/third', methods=['GET', 'POST'])
@group_permission_decorator
def third():
    """
    Function gives result of the third SQL request
    :return:
    """
    if request.method == 'GET':
        return render_template('three_request.html')

    name = request.form['name']
    sql = provider.get('request_three.sql', name = name)
    db_config = current_app.config['DB_CONFIG']
    result, schema = work_with_db(db_config, sql)

    context = {'schema': schema, 'data': result}

    if result:
        return render_template('request_three_table.html', context=context)
    else:
        return render_template('result_is_empty.html')


@request_app.route('/fourth', methods=['GET', 'POST'])
@group_permission_decorator
def fourth():
    """
    Function gives result of the fourth SQL request
    :return:
    """
    if request.method == 'GET':
        return render_template('four_request.html')
    
    year = request.form['year']
    sql = provider.get('request_four.sql', year=year)
    db_config = current_app.config['DB_CONFIG']
    result, schema = work_with_db(db_config, sql)
    context = {'schema': schema, 'data': result}

    if result:
        return render_template('request_four_table.html', context=context)
    else:
        return render_template('result_is_empty.html')

