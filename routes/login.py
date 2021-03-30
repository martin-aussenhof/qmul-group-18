from routes.database_connector import (
    connect_to_database,
    execute_select_query,
    close_database_connection,
)


def get_login(qmul_id):
    query = f"SELECT 'staff' as \"role\", password_hash from staffids WHERE qmul_staff_id = {qmul_id} union all SELECT 'student' as \"role\", password_hash from studentids WHERE qmul_student_id = {qmul_id};"
    connection = connect_to_database()
    results = execute_select_query(connection, query)
    close_database_connection(connection)
    if results:
        return results[0]
    else:
        return None