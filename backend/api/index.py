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
    print("Path:", path)  # Print the incoming path
    
    # Custom routing logic based on the path
    if path.startswith("api/sentiment"):
        print("Routing to sentiment index.py")
        # Route to sentiment index.py
        return get_sentiment()
    elif path.startswith("api/recommendations"):
        print("Routing to recommendations index.py")
        # Route to recommendations index.py
        return get_recommendations()
    elif path.startswith("api/single_recommendation"):
        print("Routing to single_recommendation index.py")
        # Route to single_recommendation index.py
        return get_single_recommendation()
    elif path.startswith("api/trending"):
        print("Routing to trending index.py")
        # Route to trending index.py
        return get_trending()
    elif path.startswith("api/stock_info"):
        print("Routing to stock_info index.py")
        # Route to stock_info index.py
        return get_stock_info()
    else:
        print("No matching route found")
        # Default route
        return Response(f"<h1>Flask</h1><p>You visited: /{path}</p>", mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
