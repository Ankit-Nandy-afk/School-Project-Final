import mysql.connector

def database_connect(host, username, password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=db_name
        )
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as err:
        print("Could not connect:",err)
        return None,None