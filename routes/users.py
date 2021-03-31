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


def users():
    if request.method == "GET":
        try:
            query = f"SELECT qmul_id, users.name as name, roles.name as role from users left join roles on users.role_id = roles.id;"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Couldn't retrieve list.", 401

    if request.method == "POST":
        required_fields = ["name", "password", "qmul_id", "role"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return (
                "Missing parameters. Please provide name, password, role (student or staff) and qmul_id",
                403,
            )

        try:
            data = request.get_json(force=True)
            role_id = 1 if data["role"] == "student" else 2
            name = data["name"]
            password_hash = generate_password_hash(data["password"])
            qmul_id = data["qmul_id"]
            query = f"INSERT INTO users (name, role_id, password_hash, qmul_id) VALUES('{name}', '{role_id}', '{password_hash}', {qmul_id});"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return (
                f"Success: {name} - has successfully been created.",
                201,
            )
        except BaseException:
            return "New user couldn't be added", 403


def user(qmul_id):
    if request.method == "GET":
        try:
            query = f"SELECT qmul_id, users.name as name, roles.name as role from users left join roles on users.role_id = roles.id where qmul_id = {qmul_id};"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "User doesn't exist.", 401

    if request.method == "PUT":
        required_fields = ["name", "password", "role", "new_qmul_id"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return (
                "Missing parameters. Please provide name, password, role (student or staff) and qmul_id",
                403,
            )
        try:
            data = request.get_json(force=True)
            role_id = 1 if data["role"] == "student" else 2
            name = data["name"]
            password_hash = generate_password_hash(data["password"])
            new_qmul_id = data["new_qmul_id"]
            query = f"UPDATE users SET name = '{name}', role_id = '{role_id}', password_hash = '{password_hash}', qmul_id = {new_qmul_id} where qmul_id = {qmul_id};"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return (
                f"{name} has successfully been updated.",
                201,
            )
        except BaseException:
            return "User couldn't be updated", 403

    if request.method == "DELETE":
        try:
            query = f"DELETE FROM users WHERE qmul_id = {qmul_id};"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return f"User {qmul_id} has successfully been deleted.", 201
        except BaseException:
            return "User doesn't exist.", 401
