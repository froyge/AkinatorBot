import psycopg2
import config as cn
from psycopg2 import Error

connection = None


def get_connection():
    '''
    Connect to database
    '''
    global connection
    if connection is None:
        try:
            connection = psycopg2.connect(user=cn.user,
                                          password=cn.password,
                                          host=cn.host,
                                          port=cn.port,
                                          database=cn.database)
            print("Connection succesful")
        except (Exception, Error) as error:
            print("Connection error:", error)
    return connection


def init_db(clear=False):
    '''
    Database initialization
    '''
    Connection = get_connection()
    cursor = Connection.cursor()
    Connection.autocommit = True

    if clear:
        cursor.execute('DROP TABLE IF EXISTS user_data')
        print("Table dropped")

    create_table_query = '''
        CREATE TABLE IF  NOT EXISTS user_data(
            user_id         INTEGER,
            first_name      TEXT,
            last_name       TEXT,
            user_name       TEXT,
            aki_lang        TEXT,
            child_mode      INTEGER
        );
    '''
    cursor.execute(create_table_query)
    Connection.commit()
    print("Table created")


def adduser(user_id: int, first_name: str, last_name: str, user_name: str) -> None:
    """
    Adding the User to the database. If user already present in the database,
    it will check for any changes in the user_name, first_name, last_name and will update if true.
    """
    Connection = get_connection()
    cursor = Connection.cursor()
    cursor.execute('SELECT distinct user_id FROM user_data where user_id = %(ud)s', {'ud': user_id})
    try:
        temp_id = cursor.fetchone()[0]
    except:
        temp_id = 0
    #print(temp_id)
    #print(type(temp_id))

    if temp_id == user_id:
        cursor.execute('UPDATE user_data SET first_name = %(fn)s,last_name = %(ls)s, user_name = %(us)s, \
                        user_id =  %(ud)s WHERE user_id =  %(ud)s',
                       {"fn": first_name, "ud": user_id, "ls": last_name, "us": user_name})
        print('User updated')
    else:
        cursor.execute('INSERT INTO user_data (user_id,first_name,last_name,user_name,aki_lang,child_mode) \
                        VALUES (%(ud)s, %(fst)s,%(lst)s, %(usn)s, %(lang)s, 1)',
                       {"ud": user_id, "fst": first_name, "lst": last_name, "usn": user_name,
                        "lang": 'en'})
        print('User inserted', user_name)
    Connection.commit()


def getlanguage(user_id: int) -> str:
    """
    Returns the Language Code of the user. (str)
    """
    Connection = get_connection()
    cursor = Connection.cursor()
    cursor.execute('SELECT aki_lang FROM user_data where user_id = %(ud)s', {'ud': user_id})
    return cursor.fetchone()[0]


def getchildmode(user_id: int) -> int:
    """
    Returns the Child mode status of the user. (str)
    """
    Connection = get_connection()
    cursor = Connection.cursor()
    cursor.execute('SELECT child_mode FROM user_data where user_id = %(ud)s', {'ud': user_id})
    return cursor.fetchone()[0]


def updatelanguage(user_id: int, lang_code: str) -> None:
    """
    Update Akinator Language for the User.
    """
    Connection = get_connection()
    cursor = Connection.cursor()
    cursor.execute('UPDATE user_data SET aki_lang = %(ln)s WHERE user_id = %(ud)s', {"ln": lang_code, 'ud': user_id})
    Connection.commit()
    print("Language updated")


def updatechildmode(user_id: int, mode: int) -> None:
    """
    Update Child Mode of the User.
    """
    Connection = get_connection()
    cursor = Connection.cursor()
    cursor.execute('UPDATE user_data SET child_mode = %(cm)s WHERE user_id = %(ud)s', {"cm": mode, 'ud': user_id})
    Connection.commit()
    print("Child mode updated")
