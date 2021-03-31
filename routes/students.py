from flask import Flask, request, jsonify
import requests
from werkzeug.security import generate_password_hash
from flask_jwt_extended import get_jwt

from routes.database_connector import (
    connect_to_database,
    execute_insert_query,
    execute_select_query,
    close_database_connection,
)


def students():
    if request.method == "GET":
        try:
            query = "SELECT id, name, qmul_id from users where role_id = 1;"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Resource doesn't exist.", 401

    if request.method == "POST":
        if not request.json or "name" not in request.json or "password" not in request.json or "qmul_id" not in request.json:
            return "Missing parameters. Please provide name, password and qmul_id", 403

        try:
            data = request.get_json(force=True)
            name = data["name"]
            password_hash = generate_password_hash(data["password"])
            qmul_id = data["qmul_id"]
            query = f"INSERT INTO users (name, role_id, password_hash, qmul_id) VALUES('{name}', 1, '{password_hash}', {qmul_id});"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return (
                f"Success: {name} - has successfully been created.",
                201,
            )
        except BaseException:
            return "New student couldn't be added", 403


def student(qmul_student_id):
    if request.method == "GET":
        try:
            query = f"SELECT qmul_student_id, student_full_name from studentids WHERE qmul_student_id = {qmul_student_id};"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Student doesn't exist.", 401
    if request.method == "DELETE":
        try:
            query1 = (
                f"DELETE FROM studentids WHERE qmul_student_id = {qmul_student_id};"
            )

            query2 = (
                f"DELETE FROM studentchoice WHERE qmul_student_id = {qmul_student_id};"
            )
            connection = connect_to_database()
            execute_insert_query(connection, query1)
            execute_insert_query(connection, query2)
            close_database_connection(connection)
            return "Student " + qmul_student_id + " successfully deleted.", 201
        except BaseException:
            return "Student doesn't exist.", 401
    if request.method == "UPDATE":
        try:
            data = request.get_json(force=True)
            topic_name = data["topic_name"]
            qmul_staff_id = data["qmul_staff_id"]
            research_area = data["research_area"]
            query = f"UPDATE studentids SET student_full_name = '{student_full_name}' WHERE qmul_student_id = {qmul_student_id};"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Student's name couldn't be updated.", 403


def studentchoices():
    if request.method == "GET":
        try:
            query = "SELECT* from studentchoice;"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Resource doesn't exist.", 401


def studentchoice(qmul_student_id):
    if request.method == "GET":
        try:
            query = (
                f"SELECT* from studentchoice WHERE qmul_student_id = {qmul_student_id};"
            )
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Student doesn't exist.", 401
    if request.method == "UPDATE":
        try:
            data = request.get_json(force=True)
            topicid = data["topicid"]
            query = f"UPDATE studentchoice SET topicid = {topicid} WHERE qmul_student_id = {qmul_student_id}, approvedid = 1, student_comment = '{student_comment}';"
            connection = connect_to_database()
            execute_insert_query(connection, query1)
            execute_insert_query(connection, query2)
            close_database_connection(connection)
            return (
                f"Topic choice for Student {qmul_student_id} has been updated successfully.",
                200,
            )
        except BaseException:
            return "Chosen topic couldn't be updated .", 403


def student_login(qmul_student_id):
    if qmul_staff_id is None:
        qmul_staff_id = 0
    query = f"SELECT password_hash from studentids WHERE qmul_student_id = {qmul_student_id};"
    connection = connect_to_database()
    results = execute_select_query(connection, query)
    close_database_connection(connection)
    if results:
        return results[0]["password_hash"]
    else:
        return None
