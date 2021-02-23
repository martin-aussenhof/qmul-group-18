from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World"


if __name__ == "__main__":
    debug_env = False
    if debug_env:
        host = "127.0.0.1"
        port = 5000
    else:
        host = "0.0.0.0"
        port = 8080
    app.run(threaded=True, host=host, port=port)
