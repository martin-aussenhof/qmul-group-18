from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
import psycopg2

# Set up Caching.
# requests_cache.install_cache("cc_g18_cache", backend="sqlite", expire_after=36000)

app = Flask(__name__)


def run_query(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(
            host="group-18.cvdzsvzawper.us-east-1.rds.amazonaws.com",
            database="postgres",
            user="postgres",
            password="Group-18",
        )
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


@app.route("/")
def home():
    return "Welcome to Group 18's REST API."


# Internal database routes.
@app.route("/datbase_ids", methods=["GET"])
def get_database_ids():
    try:
        results = run_query("SELECT* from database_id;")
        return jsonify(results), 200
    except:
        return "Resource doesn't exist.", 401


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
    except:
        return "Resource doesn't exist.", 401


@app.errorhandler(404)
def page_not_found(e):
    return "The requested route doesn't exist.", 404


if __name__ == "__main__":
    debug_env = True
    if debug_env:
        host = "127.0.0.1"
        port = 5000
    else:
        host = "0.0.0.0"
        port = 80
    app.run(threaded=True, host=host, port=port, debug=debug_env)
