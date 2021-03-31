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
    except BaseException:
        return "Couldn't connect to Database."


def close_database_connection(connection):
    if connection is not None:
        connection.close()


def execute_select_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        dict_results = list()
        for result in results:
            dict_results.append(dict(zip(headers, result)))
        cursor.close()
        return dict_results
    except (Exception, psycopg2.DatabaseError) as error:
        return error


def execute_insert_query(query):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        status = cursor.statusmessage
        cursor.close()
        close_database_connection(connection)
        return {"error": False, "status": status}
    except psycopg2.DatabaseError as error:
        return {"error": True, "status": error}
