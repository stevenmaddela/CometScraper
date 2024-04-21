#!index.py
from flask import Flask, Response

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # Everything above this line should look the same for each 
    # index.py. Modify lines below this to have different logic
    # for different routes.
    return Response(
        "<h1>Flask</h1><p>You visited: /%s</p>" % (path), mimetype="text/html"
    )