"""
Blueprint for registration of delivery and inserting data to database
"""

import os

from flask import Blueprint, session, render_template, request, current_app, redirect

from sql_provider import SQLProvider
from usedatabase import work_with_db, insert_to_db
from basket.utils import add_seller, add_to_basket, clear_basket, clear_seller
from access import group_permission_decorator

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
basket_app = Blueprint('basket', __name__, template_folder='templates')


@basket_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def choose_supplier():
    """
    Function gives the form for choosing supplier
    :return:
    """
    if request.method == 'GET':
        db_config = current_app.config['DB_CONFIG']
        SQL = provider.get('suppliers_list.sql')
        result2, schema2 = work_with_db(db_config, SQL)
        return render_template('suppliers.html', result=result2)

    name = request.form['name']
    items, _ = work_with_db(current_app.config['DB_CONFIG'], provider.get('get_supplier.sql', seller_id=name))
    print(items)

    add_seller(items)

    return redirect('/basket/list')


@basket_app.route('/list', methods=['GET', 'POST'])
@group_permission_decorator
def basket_list():
    """
    Function gives all products and your basket
    :return:
    """
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('all_products.sql'))
        print(items)
        print(current_basket)
        return render_template('basket_list.html', items=items[0], basket=current_basket)
    else:
        product_id = request.form['Product_id']
        items, _ = work_with_db(current_app.config['DB_CONFIG'],
                                provider.get('product_to_basket.sql', product_id=product_id))

        if items:
            add_to_basket(items)

        return redirect('/basket/list')


@basket_app.route('/buy')
def buy_handler():
    """
    Function inserts supply to db
    :return:
    """
    current_basket = session.get('basket', [])

    seller = session.get('seller', [])

    if current_basket:
        seller_id = seller[0]['seller_id']
        sql = provider.get('insert_to_supply.sql', seller_id=seller_id)
        db_config = current_app.config['DB_CONFIG']
        insert_to_db(db_config, sql)

        sql1 = provider.get('sort.sql')
        result, _ = work_with_db(db_config, sql1)
        supply_id = result[0]['supply_id']

        for i in current_basket:
            sql_i = provider.get('insert_to_supply_product.sql', supply_id=supply_id, product_id=i['Product_id'],
                                 S_Unit=i['Price'], S_Count=i['count'])
            insert_to_db(db_config, sql_i)

        for i in current_basket:
            sql_i2 = provider.get('insert_to_details.sql', amount=i['count'], Price=i['Price'],
                                  product_id=i['Product_id'])
            insert_to_db(db_config, sql_i2)

        clear_seller()
        clear_basket()

        return render_template('result.html', supply_id=supply_id)
    else:
        clear_seller()
        clear_basket()
        return render_template('basket_is_empty.html')


@basket_app.route('/clear-basket')
def clear_basket_handler():
    clear_basket()
    return redirect('/basket/list')


@basket_app.route('/clear')
def to_menu():
    clear_basket()
    clear_seller()
    return redirect('/')
