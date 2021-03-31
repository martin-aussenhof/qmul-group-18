from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import get_jwt

from routes.database_connector import (
    connect_to_database,
    execute_insert_query,
    execute_select_query,
    close_database_connection,
)


def choices():
    if request.method == "GET":
        try:
            query = "select topic_id, t.name as topic_name, c.qmul_id as qmul_id, u.name as student_name, approved from choices c left join users u on c.qmul_id = u.qmul_id left join topics t on c.topic_id = t.id;"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Couldn't retrieve list.", 401

    if request.method == "POST":
        required_fields = ["topic_id", "qmul_id"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return (
                "Missing parameters. Please provide topic_id and qmul_id (of student).",
                403,
            )

        try:
            data = request.get_json(force=True)
            if get_jwt()["sub"] != data["qmul_id"] and get_jwt()["role"] != "staff":
                return (
                    "Only the student themselves or a staff member can choose a topic.",
                    403,
                )
            topic_id = data["topic_id"]
            qmul_id = data["qmul_id"]
            query = f"INSERT INTO choices (topic_id, qmul_id, approved) VALUES('{topic_id}', '{qmul_id}', false);"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return (
                f"Topic has successfully been choosen.",
                201,
            )
        except BaseException:
            return "Topic couldn't be assigned", 403


def choice(qmul_id):
    if request.method == "GET":
        try:
            query = f"select topic_id, t.name as topic_name, c.qmul_id as qmul_id, u.name as student_name, approved from choices c left join users u on c.qmul_id = u.qmul_id left join topics t on c.topic_id = t.id where c.qmul_id = {qmul_id};"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "Choice doesn't exist.", 401

    if request.method == "PUT":
        required_fields = ["topic_id", "qmul_id"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return (
                "Missing parameters. Please provide topic_id and qmul_id",
                403,
            )
        try:
            data = request.get_json(force=True)
            if get_jwt()["sub"] != qmul_id and get_jwt()["role"] != "staff":
                return (
                    "Only the student themselves or a staff member can choose a topic.",
                    403,
                )
            topic_id = data["topic_id"]
            new_qmul_id = data["qmul_id"]
            query = f"UPDATE choices SET topic_id = {topic_id}, qmul_id = {new_qmul_id}, approved = false where qmul_id = {qmul_id};"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return f"Choice for student {qmul_id} has successfully been updated.", 201

        except BaseException:
            return "Choice couldn't be updated", 403

    if request.method == "DELETE":
        try:
            if get_jwt()["sub"] != qmul_id and get_jwt()["role"] != "staff":
                return (
                    "Only the student themselves or a staff member can choose a topic.",
                    403,
                )
            query = f"DELETE FROM choices WHERE qmul_id = {qmul_id};"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return f"User {qmul_id} has successfully been deleted.", 201
        except BaseException:
            return "User doesn't exist.", 401


def approve(qmul_id):
    try:
        approved = request.json["approved"]
        query = f"UPDATE choices SET approved = {approved} WHERE qmul_id = {qmul_id};"
        results = execute_insert_query(query)
        if results["error"]:
            return str(results["status"]), 403

        if approved:
            action = "approved"
        else:
            action = "disapproved"

        return f"Topic for Student {qmul_id} has been {action}.", 200
    except BaseException:
        return "Resource doesn't exist.", 401
