from flask import Flask, render_template, request, jsonify
import requests
import requests_cache

from routes.database_connector import (
    connect_to_database,
    execute_insert_query,
    execute_select_query,
    close_database_connection,
)


def staffs():
    if request.method == "GET":
        try:
            query = "SELECT qmul_staff_id, staff_full_name from staffids;"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Resource doesn't exist.", 401
    if request.method == "POST":
        if (
            not request.json
            or "staff_full_name" not in request.json
            or "qmul_staff_id" not in request.json
        ):
            return (
                "Missing parameters. Please provide staff_full_name and qmul_staff_id",
                403,
            )
        try:
            qmul_staff_id = request.json["qmul_staff_id"]
            staff_full_name = request.json["staff_full_name"]
            query = f"INSERT INTO staffids (qmul_staff_id, staff_full_name) VALUES({str(qmul_staff_id)}, '{staff_full_name}');"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return (
                f"Success: {str(qmul_staff_id)} - {staff_full_name} has successfully been created.",
                201,
            )
        except BaseException:
            return "Staff entry couldn't be created.", 403


def staff(qmul_staff_id):
    if request.method == "GET":
        try:
            query = f"SELECT qmul_staff_id, staff_full_name from staffids WHERE qmul_staff_id = {qmul_staff_id};"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Resource doesn't exist.", 401
    if request.method == "DELETE":
        try:
            query = f"UPDATE topics SET qmul_staff_id = 999999999 where qmul_staff_id = {qmul_staff_id} and topicid != 0;"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)

            query = f"DELETE from staffids WHERE qmul_staff_id = {qmul_staff_id};"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return f"Staff ID: {qmul_staff_id} has been deleted.", 200
        except BaseException:
            return "Resource doesn't exist.", 401
    if request.method == "PUT":
        try:
            staff_full_name = request.json["staff_full_name"]
            query = f"UPDATE staffids SET staff_full_name = '{staff_full_name}' where qmul_staff_id = {qmul_staff_id};"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)

            return f"Staff ID: {qmul_staff_id} has been updated.", 200
        except BaseException:
            return "Resource doesn't exist.", 401


def approve(qmul_student_id):
    try:
        approvedid = request.json["approvedid"]
        query = f"UPDATE studentchoice SET approvedid = {approvedid} WHERE qmul_student_id = {qmul_student_id};"
        connection = connect_to_database()
        execute_insert_query(connection, query)
        close_database_connection(connection)

        if approvedid == 2:
            action = "approved"
        else:
            action = "disapproved"

        return f"Topic for Student {qmul_student_id} has been {action}.", 200
    except BaseException:
        return "Resource doesn't exist.", 401


def staff_login(qmul_staff_id):
    if qmul_staff_id is None:
        qmul_staff_id = 0
    query = f"SELECT password_hash from staffids WHERE qmul_staff_id = {qmul_staff_id};"
    connection = connect_to_database()
    results = execute_select_query(connection, query)
    close_database_connection(connection)
    if results:
        return results[0]["password_hash"]
    else:
        return None