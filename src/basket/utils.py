"""
Utils for basket
"""

from flask import session


def add_seller(item):
    sellers = session.get('seller', [])
    print(session)
    for seller in item:
        sellers.append(seller)

    session['seller'] = sellers


def add_to_basket(items):
    """
    Function adds products to basket and remembered amount of particular product
    :param items:
    :return:
    """
    basket = session.get('basket', [])
    count = 1
    for item in items:
        item.update(dict(count=count))

    for item in items:
        key = True
        for i in basket:
            if item['Product_id'] == i['Product_id']:
                i['count'] += 1
                key = False
        if key:
            basket.append(item)
    session['basket'] = basket


def clear_basket():
    if 'basket' in session:
        session.pop('basket')


def clear_seller():
    if 'seller' in session:
        session.pop('seller')