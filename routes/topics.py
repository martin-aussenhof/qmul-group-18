from flask import Flask, render_template, request, jsonify
import requests
from flask_jwt_extended import get_jwt_identity

from routes.database_connector import (
    connect_to_database,
    execute_insert_query,
    execute_select_query,
    close_database_connection,
)


def get_topics():
    try:
        query = "SELECT* from topics;"
        connection = connect_to_database()
        results = execute_select_query(connection, query)
        close_database_connection(connection)
        results = hot_or_not(results)
        return jsonify(results), 200
    except BaseException:
        return "Resource doesn't exist.", 401


def post_topics():
    try:
        data = request.get_json(force=True)
        topicid = data["topicid"]
        topic_name = data["topic_name"]
        qmul_staff_id = data["qmul_staff_id"]
        research_area = data["research_area"]
        query = f"INSERT INTO topics (topicid, topic_name, qmul_staff_id, research_area) VALUES({topicid}, '{topic_name}', {qmul_staff_id}, '{research_area}')"
        connection = connect_to_database()
        execute_insert_query(connection, query)
        close_database_connection(connection)
        return "New topic created", 201
    except BaseException:
        return "New topic couldn't be created", 403


def get_topic(id):

    if get_jwt()["role"] == "student" and qmul_student_id != get_jwt()[
            "qmul_student_id"]:
        return jsonify(msg="You can only view your own entry!"), 403
    try:
        query = f"select id, topics.name, staff.name supervisor, research_area from topics left join staff on topics.qmul_staff_id = staff.qmul_staff_id where id not in (0,9);"
        connection = connect_to_database()
        results = execute_select_query(connection, query)
        close_database_connection(connection)
        results = hot_or_not(results)
        return jsonify(results), 200
    except BaseException:
        return "Topic doesn't exist or an error occured.", 401


def topic(id):
    if request.method == "DELETE":
        try:
            query = f"DELETE FROM topics WHERE topicid = {id};"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return "Topic " + id + " successfully deleted.", 201
        except BaseException:
            return "Topic doesn't exist.", 401
    if request.method == "PUT":
        try:
            data = request.get_json(force=True)
            name = data["name"]
            qmul_staff_id = data["qmul_staff_id"]
            research_area = data["research_area"]
            query = f"UPDATE topics SET name = '{name}', qmul_staff_id = {qmul_staff_id}, research_area = '{research_area}' WHERE id = {id};"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return "Topic {topic_name} has been updated.", 200
        except BaseException:
            return "Topic couldn't be updated .", 403


def hot_or_not(results):
    for index, result in enumerate(results):
        topic_name = result["topic_name"]
        test_url = f"https://core.ac.uk:443/api-v2/search/{topic_name}?page=1&pageSize=10&apiKey=EJAX4BU5wNxsD8HPG23ynkt1M6Oirm9T"
        resp = requests.get(test_url)
        if resp.ok:
            result_list = list(results[index])
            if resp.json()["totalHits"] > 50000000:
                hot_factor = "hot"
            else:
                hot_factor = "cold"
            results[index]["hot_factor"] = hot_factor
        else:
            results[index]["hot_factor"] = "unknown"
    return results
