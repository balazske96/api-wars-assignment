import psycopg2
import psycopg2.extras
import os

def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('loujrykxrivlnz')
    password = os.environ.get('a7a778fad0278bc72eac4d8b56ecbd9a60fa76c14f03b72946eb4734d7ab135b')
    host = os.environ.get('ec2-54-228-252-67.eu-west-1.compute.amazonaws.com')
    database_name = os.environ.get('droc7aa4e8k5')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')

def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper
