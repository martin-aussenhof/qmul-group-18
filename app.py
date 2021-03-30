from functools import wraps
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
import requests
import requests_cache
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    verify_jwt_in_request,
    get_jwt_identity,
    get_jwt,
    jwt_required,
    JWTManager,
)

from routes.students import (
    students,
    student,
    studentchoices,
    studentchoice,
    student_login,
)
from routes.staff import staffs, staff, approve, staff_login
from routes.topics import get_topics, post_topics, topic, hot_or_not
from routes.login import get_login

# Set up Caching.
requests_cache.install_cache("cc_g18_cache", backend="sqlite", expire_after=36000)

# Set up App.
app = Flask(__name__)

app.secret_key = "standupforyourvaluesinlifebeforetheyretakenfromyou"
app.config["JWT_SECRET_KEY"] = "standupforyourvaluesinlifebeforetheyretakenfromyou"
jwt = JWTManager(app)


def staff_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == "staff":
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="This route is for staff members only!"), 403

        return decorator

    return wrapper


# Add Routes
app.add_url_rule(
    "/students",
    view_func=staff_required()(students),
    methods=["GET", "POST"],
)

app.add_url_rule(
    "/student/<qmul_student_id>",
    view_func=staff_required()(student),
    methods=["GET", "DELETE", "PUT"],
)

app.add_url_rule(
    "/studentchoice",
    view_func=staff_required()(studentchoices),
    methods=["GET"],
)
app.add_url_rule(
    "/studentchoice/<qmul_student_id>",
    view_func=staff_required()(studentchoice),
    methods=["GET", "PUT"],
)

app.add_url_rule(
    "/staff",
    view_func=staff_required()(staffs),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/staff/<qmul_staff_id>",
    view_func=staff_required()(staff),
    methods=["GET", "DELETE", "PUT"],
)
app.add_url_rule(
    "/approve/<qmul_staff_id>",
    view_func=staff_required()(approve),
    methods=["PUT"],
)

app.add_url_rule(
    "/topics",
    view_func=jwt_required()(get_topics),
    methods=["GET"],
)

app.add_url_rule(
    "/topics",
    view_func=staff_required()(post_topics),
    methods=["POST"],
)

app.add_url_rule(
    "/topic/<id>",
    view_func=jwt_required()(get_topic),
    methods=["GET"],
)

app.add_url_rule(
    "/topics/<topicid>",
    view_func=staff_required()(topic),
    methods=["DELETE", "PUT"],
)


@app.route("/")
def home():
    return "Welcome to Group 18's REST API."


@app.errorhandler(404)
def page_not_found(e):
    return "The requested route doesn't exist.", 404


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("qmul_id", None)
    password = request.form.get("password", None)
    if username.isnumeric():
        login = get_login(username)
        if login and check_password_hash(login["password_hash"], password):
            access_token = create_access_token(
                identity=username, additional_claims={"role": login["role"]}
            )
            return render_template("access_token.html", access_token=access_token)
    flash("Please check your login details and try again.")
    return redirect(url_for("login"))


# Authentication
# @basic_auth.verify_password
# def verify_password(username, password):
#     try:
#         password_hash = student_login(username)
#     except:
#         password_hash = None
#         pass

#     if password_hash is None:
#         try:
#             password_hash = staff_login(username)
#         except:
#             pass

#     if password_hash and check_password_hash(password_hash, password):
#         return username


# @token_auth.verify_token
# def verify_token(token):
#     try:
#         data = jws.loads(token)
#     except:  # noqa: E722
#         return False
#     if "qmul_id" in data:
#         return data["qmul_id"]


# @multi_auth.get_user_roles
# def get_user_roles(username):
#     try:
#         student = student_login(username)
#         if student:
#             return "student"
#     except:
#         pass

#     try:
#         staff = staff_login(username)
#         if staff:
#             return "staff"
#     except:
#         pass


# @app.route("/authentication")
# @multi_auth.login_required(role=["student", "staff"])
# def generate_token():
#     token = jws.dumps({"qmul_id": multi_auth.current_user()})
#     return f"Your token is: <strong>{token.decode('utf-8')}</strong>"


# if __name__ == "__main__":
#     debug_env = True
#     if debug_env:
#         host = "127.0.0.1"
#         port = 5000
#     else:
#         host = "0.0.0.0"
#         port = 80
#     app.run(threaded=True, host=host, port=port, debug=debug_env)
