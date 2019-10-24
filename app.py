"""
Flask application for demonstrating the functionality of Percolate Developer Platform
applications.
"""
import os
import pprint

from flask import Flask, request, render_template
from jose import ExpiredSignatureError, JWTError, jwt


app = Flask(__name__)


@app.route("/install", methods=["POST"])
@app.route("/uninstall", methods=["POST"])
@app.route("/enable", methods=["POST"])
@app.route("/disable", methods=["POST"])
@app.route("/update", methods=["POST"])
def generic_lifecycle_endpoint():
    app.logger.info("Got lifecycle web request")
    print(
        '"{}" endpoint called with data: \n{}'.format(
            request.base_url.split("/")[-1], request.get_json()
        )
    )
    return "OK\n"


@app.route("/")
def hello():
    return "hi\n"


@app.route("/top_nav", methods=["GET"])
def splash_screen():
    token = request.args.get("jwt")
    app_secret = os.environ.get("APP_SECRET")
    audience = os.environ.get("APP_AUDIENCE")

    data = {"Info": "No user info found."}
    if app_secret and token and audience:
        data = verify(token, app_secret, audience, html=False)
    return render_template("index.html", data=data)


show_token_html = (
    "<h1>jwt</h1> <pre>{token}</pre> <h1>decoded</h1> <pre>{decoded_token}</pre>"
)
show_invalid_token_html = "<h1>invalid jwt</h1> <pre>{token}</pre>"
show_expired_token_html = "<h1>Expired jwt</h1> <pre>{token}</pre>"


def verify(token, secret, audience, html=True):
    try:
        payload = jwt.decode(
            token,
            secret,
            audience=audience,
            options={"verify_signature": True, "verify_exp": True},
        )
    except ExpiredSignatureError:
        return (
            show_token_html.format(token=token) if html else {"Error": "Token expired"}
        )
    except JWTError:
        return (
            show_invalid_token_html.format(token=token)
            if html
            else {"Error": "Invalid token"}
        )

    return (
        show_token_html.format(
            token=token, decoded_token=pprint.pformat(payload, indent=4)
        )
        if html
        else payload
    )


# object handles
@app.route("/campaign", methods=["GET"])
@app.route("/content", methods=["GET"])
@app.route("/asset", methods=["GET"])
@app.route("/request", methods=["GET"])
@app.route("/task", methods=["GET"])
@app.route("/settings", methods=["GET"])
def generic_ui_component_endpoint():
    token = request.args.get("jwt")
    app_secret = os.environ.get("APP_SECRET")
    audience = os.environ.get("APP_AUDIENCE")

    if not app_secret:
        return "<h1>No app secret defined.</h1>"
    elif not token:
        return "<h1>Acess token is required.</h1>"
    else:
        return verify(token, app_secret, audience)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
