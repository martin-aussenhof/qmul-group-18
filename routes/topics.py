from flask import Flask, render_template, request, jsonify
import requests
from flask_jwt_extended import get_jwt_identity

from routes.database_connector import (
    connect_to_database,
    execute_insert_query,
    execute_select_query,
    close_database_connection,
)


def topics():
    if request.method == "GET":
        try:
            query = f"SELECT id, topics.name as name, users.name as supervisor, topics.research_area as research_area from topics left join users on topics.supervisor = users.qmul_id;"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            results = hot_or_not(results)
            return jsonify(results), 200
        except BaseException:
            return "Couldn't retrieve list.", 401

    if request.method == "POST":
        required_fields = ["topic", "supervisor", "research_area"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return (
                "Missing parameters. Please provide topic, supervisor (qmul_id) and research_area",
                403,
            )

        try:
            data = request.get_json(force=True)
            name = data["topic"]
            supervisor = data["supervisor"]
            research_area = data["research_area"]
            query = f"INSERT INTO topics (name, supervisor, research_area) VALUES('{name}', '{supervisor}', '{research_area}');"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return (
                f"{name} - has successfully been created.",
                201,
            )
        except BaseException:
            return "New topic couldn't be added", 403


def topic(id):
    if request.method == "GET":
        try:
            query = f"SELECT id, topics.name as name, users.name as supervisor, topics.research_area as research_area from topics left join users on topics.supervisor = users.qmul_id where id = {id};"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except BaseException:
            return "User doesn't exist.", 401

    if request.method == "PUT":
        required_fields = ["topic", "supervisor", "research_area"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return (
                "Missing parameters. Please provide topic, supervisor (qmul_id) and research_area",
                403,
            )
        try:
            data = request.get_json(force=True)
            name = data["topic"]
            supervisor = data["supervisor"]
            research_area = data["research_area"]
            query = f"UPDATE topics SET name = '{name}', supervisor = {supervisor}, research_area = '{research_area}' where id = {id};"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return (
                f"{name} has successfully been updated.",
                201,
            )
        except BaseException:
            return "Topic couldn't be updated", 403

    if request.method == "DELETE":
        try:
            query = f"DELETE FROM topics WHERE id = {id};"
            results = execute_insert_query(query)
            if results["error"]:
                return str(results["status"]), 403
            return f"Topic {id} has successfully been deleted.", 201
        except BaseException:
            return "Topic doesn't exist.", 401


def hot_or_not(results):
    for index, result in enumerate(results):
        topic_name = result["name"]
        test_url = f"https://core.ac.uk:443/api-v2/search/{topic_name}?page=1&pageSize=10&apiKey=EJAX4BU5wNxsD8HPG23ynkt1M6Oirm9T"
        resp = requests.get(test_url)
        if resp.ok:
            result_list = list(results[index])
            if resp.json()["totalHits"] > 100000000:
                hot_factor = "hot"
            else:
                hot_factor = "cold"
            results[index]["hot_factor"] = hot_factor
        else:
            results[index]["hot_factor"] = "unknown"
    return results
