from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
from routes.database_connector import connect_to_database, execute_insert_query, execute_select_query, close_database_connection
from routes.staff import staffs, staff, choice, approve

# Set up Caching.
# requests_cache.install_cache("cc_g18_cache", backend="sqlite", expire_after=36000)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


app.add_url_rule('/staff', view_func=staffs, methods=["GET", "POST"])
app.add_url_rule(
    '/staff/<qmul_staff_id>',
    view_func=staff,
    methods=[
        "GET",
        "DELETE",
        "PUT"])
app.add_url_rule(
    '/approve/<qmul_staff_id>',
    view_func=approve,
    methods=["PUT"])
app.add_url_rule('/choice/<qmul_staff_id>', view_func=choice, methods=["PUT"])


@app.route("/")
def home():
    return "Welcome to Group 18's REST API."


@app.errorhandler(404)
def page_not_found(e):
    return "The requested route doesn't exist.", 404

# External API routes.


@app.route("/science", methods=["GET"])
def science():
    try:
        test_url = "https://core.ac.udd:443/api-v2/search/computing?page=1&pageSize=10&apiKey=EJAX4BU5wNxsD8HPG23ynkt1M6Oirm9T"
        resp = requests.get(test_url)
        if resp.ok:
            return resp.json(), 200
        else:
            return resp.reason, 401
    except BaseException:
        return "Resource doesn't exist.", 401


if __name__ == "__main__":
    debug_env = True
    if debug_env:
        host = "127.0.0.1"
        port = 5000
    else:
        host = "0.0.0.0"
        port = 80
    app.run(threaded=True, host=host, port=port, debug=debug_env)
