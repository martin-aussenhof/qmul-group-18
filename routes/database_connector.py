import psycopg2


def connect_to_database():
    """ Connect to the PostgreSQL database server """
    connection = None
    try:
        connection = psycopg2.connect(
            host="group-18.cvdzsvzawper.us-east-1.rds.amazonaws.com",
            database="postgres",
            user="postgres",
            password="Group-18",
        )
        return connection
    except:
        return "Couldn't connect to Database."


def execute_select_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def execute_insert_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_database_connection(connection):
    if connection is not None:
        connection.close()
