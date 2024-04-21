from flask import Flask, Response, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    if path == "stock_info":
        return get_stock_info()
    else:
        return Response(
            "<h1>Flask</h1><p>Route not found: /%s</p>" % (path), mimetype="text/html"
        )

def get_stock_info():
    # Retrieve the stock ticker from the query parameters
    stock_ticker = request.args.get('ticker')
    
    stock = yf.Ticker(stock_ticker)
    # Get the intraday data for the current day
    intraday_data = stock.history(period='1d', interval='1m')

    # Access the most recent closing price (current value)
    current_value = intraday_data['Close'].iloc[-1]

    # Access the closing price from yesterday (second-to-last data point)
    historical_data = stock.history(period='2d', interval='1d')
    yesterday_close = historical_data['Close'].iloc[-2]

    # Calculate the change in dollars
    change_in_dollars = current_value - yesterday_close

    # Calculate the percent change
    percent_change = (change_in_dollars / yesterday_close) * 100

    # Prepare the HTML response
    html_response = f"<h1>Stock Information for {stock_ticker}</h1>"
    html_response += "<h2>Current Value</h2>"
    html_response += f"<p>Value: {current_value}</p>"
    html_response += "<h2>Change</h2>"
    html_response += f"<p>Change in Dollars: {change_in_dollars}</p>"
    html_response += f"<p>Percent Change: {percent_change}</p>"

    return Response(html_response, mimetype="text/html")

if __name__ == '__main__':
    app.run(debug=True)
