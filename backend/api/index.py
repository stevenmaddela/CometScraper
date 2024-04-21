from flask import Flask, Response
from sentiment.index import get_sentiment
from recommendations.index import get_recommendations
from single_recommendation.index import get_single_recommendation
from trending.index import get_trending
from stock_info.index import get_stock_info

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # Custom routing logic based on the path
    if path.startswith("api/sentiment"):
        # Route to sentiment index.py
        return get_sentiment()
    elif path.startswith("api/recommendations"):
        # Route to recommendations index.py
        return get_recommendations()
    elif path.startswith("api/single_recommendation"):
        # Route to single_recommendation index.py
        return get_single_recommendation()
    elif path.startswith("api/trending"):
        # Route to trending index.py
        return get_trending()
    elif path.startswith("api/stock_info"):
        # Route to stock_info index.py
        return get_stock_info()
    else:
        # Default route
        return Response(f"<h1>Flask</h1><p>You visited: /{path}</p>", mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
