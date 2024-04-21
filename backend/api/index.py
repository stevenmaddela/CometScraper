# api/index.py
from flask import Flask, Response
from pathlib import Path

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # Get the path to the requested function's index.py file
    function_path = Path(__file__).resolve().parent / path / "index.py"

    # Check if the file exists
    if function_path.exists():
        # If it exists, import and run the Flask app from that file
        module_name = function_path.parent.name + ".index"
        module = __import__(module_name, fromlist=["app"])
        return module.app()

    # If the file does not exist, return a 404 response
    return Response("<h1>Not Found</h1>", status=404, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
