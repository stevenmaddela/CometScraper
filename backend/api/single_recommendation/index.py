from flask import Flask, Response, jsonify, request
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
import random
import os
import json
import time

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    if path == "single_recommendation":
        return get_single_recommendation()
    else:
        return Response(
            "<h1>Flask</h1><p>Route not found: /%s</p>" % (path), mimetype="text/html"
        )

def get_single_recommendation():
    def calculate_sector_distribution(stock_list):
        sector_counts = {}
        sector_info = {}

        # Read sector information from StockInfo.txt
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "data", "StockInfo.txt")
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) >= 3:
                    sector = parts[-1]  # Get the last part as sector
                    sector_counts[sector] = sector_counts.get(sector, 0)
                    sector_info[parts[0]] = sector  # Store sector information for each stock

        # Count occurrences of each sector in the input stock list
        for stock in stock_list:
            sector = sector_info.get(stock, "Unknown")
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

        # Calculate the percentage distribution of sectors
        total_stocks = len(stock_list)
        sector_distribution = {sector: (count / total_stocks) * 100 for sector, count in sector_counts.items()}

        return sector_distribution, sector_info

    def pick_stocks_based_on_distribution(sector_distribution, total_stocks=20, existing_stocks=[]):
        picked_stocks = []

        # Pick stocks based on sector distribution percentages
        for sector, percentage in sector_distribution.items():
            num_stocks = int(total_stocks * (percentage / 100))
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, "..", "data", "StockInfo.txt")
            with open(file_path, "r") as file:
                stocks_in_sector = [line.split(", ")[0] for line in file if line.strip().endswith(sector)]
                
                # Exclude stocks that are already in existing_stocks
                filtered_stocks = [stock for stock in stocks_in_sector if stock not in existing_stocks]
                
                picked_stocks.extend(random.sample(filtered_stocks, min(num_stocks, len(filtered_stocks))))

        return picked_stocks

    def get_stats(ticker):
        info = yf.Tickers(ticker).tickers[ticker].info
        return [ticker, info['currentPrice']]
    
    def get_change(ticker):
        stock = yf.Ticker(ticker)
        
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
        
        return change_in_dollars, percent_change
    
    # Get the array of arrays received from the URL
    array_of_arrays_str = request.args.get('arrayOfArrays')
    FullStock_list = json.loads(array_of_arrays_str)
    print("Array of arrays received:", FullStock_list)

    # Extract stock tickers from the received data
    stock_list = [stock[0] for stock in FullStock_list]

    # Calculate the total price and count of stocks
    total_price = sum(stock[1] for stock in FullStock_list)
    total_stocks = len(FullStock_list)

    # Calculate the average price
    average_price = total_price / total_stocks

    # Calculate sector distribution and sector information
    sector_distribution, sector_info = calculate_sector_distribution(stock_list)

    # Pick stocks based on sector distribution
    picked_stocks = pick_stocks_based_on_distribution(sector_distribution, existing_stocks=stock_list)

    # Fetch stats for the picked stocks using multithreading
    start_time = time.time()
    stats_array = []

    # Fetch stats for the picked stocks using multithreading
    with ThreadPoolExecutor() as executor:
        for stats in executor.map(get_stats, picked_stocks):
            stats_array.append(stats)

    # Sort the stats_array based on the absolute difference between each stock's price and the average_price
    sorted_stats = sorted(stats_array, key=lambda x: abs(x[1] - average_price))

    # Select the top 1 closest stock
    closest_stock = sorted_stats[0]

    end_time = time.time()
    print("Average price of each stock:", average_price)
    print(f"The program took {end_time - start_time:.2f} seconds.")
    print("Information for the closest stock:")
    
    # Get the ticker, price, price change, and percent change for the closest stock
    ticker, price = closest_stock
    dchange, pchange = get_change(ticker)
    sector = sector_info.get(ticker, "Unknown")

    # Prepare the HTML response
    html_response = f"<h1>Single Stock Recommendation</h1>"
    html_response += "<h2>Stock Information</h2>"
    html_response += f"<p>Ticker: {ticker}</p>"
    html_response += f"<p>Price: {price}</p>"
    html_response += f"<p>Price Change: {dchange}</p>"
    html_response += f"<p>Percent Change: {pchange}</p>"
    html_response += f"<p>Sector: {sector}</p>"

    return Response(html_response, mimetype="text/html")

if __name__ == '__main__':
    app.run(debug=True, port=5002)
