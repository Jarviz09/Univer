from functools import wraps

from flask import session, request, current_app, render_template


def group_validation():
    group_name = session.get('group_name', '')
    if group_name:
        return True
    else:
        return False


def group_validation_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_validation():
            return f(*args, **kwargs)
        else:
            return 'Permission Denied'

    return wrapper


def group_permission_validation(app: str = None):
    """
    Function for checking access to blueprints
    :return:
    """
    access_config = current_app.config['ACCESS_CONFIG']
    group_name = session.get('group_name', 'unauthorized')

    # request.endpoint = /auth/login => 'auth.login_page'
    # request.endpoint = /user/name => 'select_user' = ['select_user']

    if app is None:
        endpoint = request.endpoint
    else:
        endpoint = app

    target_app = "" if len(endpoint.split('.')) == 1 else endpoint.split('.')[0]
    print(group_name)
    print(endpoint)
    if group_name in access_config and target_app in access_config[group_name]:
        return True
    return False


def group_permission_decorator(f):
    """
    Decorator for checking access to blueprints
    :param f:
    :return:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return f(*args, **kwargs)
        return render_template('forbidden.html')

    return wrapper
