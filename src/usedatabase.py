from typing import Dict

from pymysql import connect
from pymysql.err import InterfaceError, OperationalError, IntegrityError


class UseDatabase:

    """
    A class for connecting to database
    """

    def __init__(self, config: dict):
        """
        Constructs all necessary attributes for db
        """
        self.config = config

    def __enter__(self):
        """
        Connect with db
        Check for mistakes

        returns:
        Codes of mistakes if exist
        """

        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except InterfaceError as err:
            return err
        except OperationalError as err:
            if err.args[0] == 1049:
                print('Неверное имя базы данных\n')
            if err.args[0] == 1045:
                print('Неверное имя пользователя или пароль\n')
            if err.args[0] == 2003:
                print('Неверное имя хоста\n')
            return None

    def __exit__(self, exc_type, exc_value, exc_trace):

        if exc_value is None:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        elif exc_value == 'cur':
            print('Курсор не создан\n')
        elif exc_value.args[0] == 1046:
            print('Неправильный синтаксис в SQL запросе\n')
        elif exc_value.args[0] == 1146:
            print('Неправильное название таблицы\n')
        elif exc_value.args[0] == 1054:
            print('Неправильное название поля\n')
        return True


def work_with_db(config: Dict, sql: str):
    """
    result of SQL request
    :param config:
    :param sql:
    :return:
    """
    with UseDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('is none')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
    return result, schema


def get_supplier_id(config: Dict, sql: str):
    with UseDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('is none')
        cursor.execute(sql)


def insert_to_db(dbconfig, _sql):
    """
    inserts info to db
    :param dbconfig:
    :param _sql:
    :return:
    """
    try:
        with UseDatabase(dbconfig) as cursor:
            cursor.execute(_sql)
        return True
    except IntegrityError:
        return False
