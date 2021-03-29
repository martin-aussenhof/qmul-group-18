from flask import Flask, render_template, request, jsonify
import requests

from routes.database_connector import (
    connect_to_database,
    execute_insert_query,
    execute_select_query,
    close_database_connection,
)


def topics():
    if request.method == "GET":
        try:
            query = "SELECT* from topics;"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except:
            return "Resource doesn't exist.", 401
    if request.method == "POST":
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
        except:
            return "New topic couldn't be created", 403


def topic(topicid):
    if request.method == "GET":
        try:
            query = f"SELECT* from topics WHERE topicid = {topicid};"
            connection = connect_to_database()
            results = execute_select_query(connection, query)
            close_database_connection(connection)
            return jsonify(results), 200
        except:
            return "Topic doesn't exist.", 401
    if request.method == "DELETE":
        try:
            query = f"DELETE FROM topics WHERE topicid = {topicid};"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return "Topic " + topicid + " successfully deleted.", 201
        except:
            return "Topic doesn't exist.", 401
    if request.method == "PUT":
        try:
            data = request.get_json(force=True)
            topic_name = data["topic_name"]
            qmul_staff_id = data["qmul_staff_id"]
            research_area = data["research_area"]
            query = f"UPDATE topics SET topic_name = '{topic_name}', qmul_staff_id = {qmul_staff_id}, research_area = '{research_area}' WHERE topicid = {topicid};"
            connection = connect_to_database()
            execute_insert_query(connection, query)
            close_database_connection(connection)
            return "Topic {topic_name} has been updated.", 200
        except:
            return "Topic couldn't be updated .", 403