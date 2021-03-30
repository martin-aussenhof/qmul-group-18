from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
from routes.database_connector import (
    connect_to_database,
    execute_insert_query,
    execute_select_query,
    close_database_connection,
)

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as JWS
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth


# from passlib.apps import custom_app_context as pwd_context

from routes.students import (
    students,
    student,
    studentchoices,
    studentchoice,
    student_login,
)
from routes.staff import staffs, staff, approve, staff_login
from routes.topics import topics, topic, hot_or_not


# Set up Caching.
requests_cache.install_cache("cc_g18_cache", backend="sqlite", expire_after=36000)

# Set up App.
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
jws = JWS(app.config["SECRET_KEY"], expires_in=3600)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth("Bearer")
multi_auth = MultiAuth(basic_auth, token_auth)

# Add Routes
app.add_url_rule(
    "/student",
    view_func=multi_auth.login_required(role="staff")(students),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/student/<qmul_student_id>",
    view_func=multi_auth.login_required(role=["staff", "student"])(student),
    methods=["GET", "DELETE", "PUT"],
)

app.add_url_rule(
    "/studentchoice",
    view_func=multi_auth.login_required(role="staff")(studentchoices),
    methods=["GET"],
)
app.add_url_rule(
    "/studentchoice/<qmul_student_id>",
    view_func=multi_auth.login_required(role="staff")(studentchoice),
    methods=["GET", "PUT"],
)

app.add_url_rule(
    "/staff",
    view_func=multi_auth.login_required(role="staff")(staffs),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/staff/<qmul_staff_id>",
    view_func=multi_auth.login_required(role="staff")(staff),
    methods=["GET", "DELETE", "PUT"],
)
app.add_url_rule(
    "/approve/<qmul_staff_id>",
    view_func=multi_auth.login_required(role="staff")(approve),
    methods=["PUT"],
)

app.add_url_rule(
    "/topics",
    view_func=multi_auth.login_required(role=["staff", "student"])(topics),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/topics/<topicid>",
    view_func=multi_auth.login_required(role=["staff", "student"])(topic),
    methods=["GET", "DELETE", "PUT"],
)
app.add_url_rule(
    "/hot_or_not/<topicname>",
    view_func=multi_auth.login_required(role=["staff", "student"])(hot_or_not),
    methods=["GET"],
)


@app.route("/")
def home():
    return "Welcome to Group 18's REST API."


@app.errorhandler(404)
def page_not_found(e):
    return "The requested route doesn't exist.", 404


# Authentication
@basic_auth.verify_password
def verify_password(username, password):
    try:
        password_hash = student_login(username)
    except:
        password_hash = None
        pass

    if password_hash is None:
        try:
            password_hash = staff_login(username)
        except:
            pass

    if password_hash and check_password_hash(password_hash, password):
        return username


@token_auth.verify_token
def verify_token(token):
    try:
        data = jws.loads(token)
    except:  # noqa: E722
        return False
    if "qmul_id" in data:
        return data["qmul_id"]


@basic_auth.get_user_roles
def get_user_roles(username):
    try:
        student = student_login(username)
        if student:
            return "student"
    except:
        pass

    try:
        staff = staff_login(username)
        if staff:
            return "staff"
    except:
        pass


@app.route("/authentication")
@multi_auth.login_required(role=["student", "staff"])
def generate_token():
    token = jws.dumps({"qmul_id": multi_auth.current_user()})
    return f"Your token is: <strong>{token.decode('utf-8')}</strong>"


if __name__ == "__main__":
    debug_env = True
    if debug_env:
        host = "127.0.0.1"
        port = 5000
    else:
        host = "0.0.0.0"
        port = 80
    app.run(threaded=True, host=host, port=port, debug=debug_env)
