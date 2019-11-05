import os
import pprint

from flask import Flask, request
from jose import ExpiredSignatureError, JWTError, jwt

app = Flask(__name__, static_url_path="/", static_folder="public")

SHOW_TOKEN_HTML = """
    <h1>jwt</h1>
    <pre>{token}</pre>
    <h1>decoded</h1>
    <pre>{decoded_token}</pre>
"""
SHOW_INVALID_TOKEN_HTML = """
    <h1>invalid jwt</h1>
    <pre>{token}</pre>
"""


@app.route("/top_nav", methods=["GET"])
@app.route("/campaign", methods=["GET"])
@app.route("/content", methods=["GET"])
@app.route("/asset", methods=["GET"])
@app.route("/request", methods=["GET"])
@app.route("/task", methods=["GET"])
@app.route("/settings", methods=["GET"])
def echo_jwt():
    app_secret = os.environ.get("APP_SECRET")
    token = request.args.get("jwt")

    if not app_secret:
        return "No APP_SECRET defined"
    if not token:
        return "No JWT found in request"

    try:
        payload = jwt.decode(token, secret, options={"verify_aud": False})
    except JWTError:
        return SHOW_INVALID_TOKEN_HTML.format(token=token)

    return SHOW_TOKEN_HTML.format(
        token=token, decoded_token=pprint.pformat(payload, indent=4)
    )


@app.route("/install", methods=["POST"])
@app.route("/uninstall", methods=["POST"])
@app.route("/enable", methods=["POST"])
@app.route("/disable", methods=["POST"])
@app.route("/update", methods=["POST"])
@app.route("/upgrade", methods=["POST"])
def lifecycle_callback():
    message = '"{}" lifecycle callback endpoint called with data: \n{}'.format(
        request.base_url.split("/")[-1], request.get_json()
    )
    app.logger.info(message)
    return "OK\n"


@app.route("/")
def hello():
    return "hi\n"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
