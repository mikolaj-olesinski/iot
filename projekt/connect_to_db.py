import mysql.connector
#pip install mysql-connector-python

def connect_to_database(host='localhost', user='root', password='', database='parking'):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        raise
