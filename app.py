"""
Flask application for demonstrating the functionality of Percolate Developer Platform
applications.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/install", methods=["POST"])
@app.route("/uninstall", methods=["POST"])
@app.route("/enable", methods=["POST"])
@app.route("/disable", methods=["POST"])
@app.route("/update", methods=["POST"])
def generic_endpoint():
    print(
        '"{}" endpoint called with data: \n{}'.format(
            request.base_url.split("/")[-1], request.get_json()
        )
    )
    return "OK\n"


@app.route("/")
def hello():
    return "hi\n"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
