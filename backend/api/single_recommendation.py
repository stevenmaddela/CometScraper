from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
import random
import os

class SingleRecommendationHandler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.send_header('Access-Control-Allow-Methods', 'GET')  # Allow only GET requests
        self.end_headers()
        
        # Function to get stock stats
        def get_stats(ticker):
            info = yf.Tickers(ticker).tickers[ticker].info
            return [ticker, info['currentPrice']]

        # Retrieve the list of stocks from the query parameters
        array_of_arrays_str = self.path.split('/')[-1]
        FullStock_list = json.loads(array_of_arrays_str)

        stock_list = [stock[0] for stock in FullStock_list]

        # Calculate the total price and count of stocks
        total_price = sum(stock[1] for stock in FullStock_list)
        total_stocks = len(FullStock_list)

        # Calculate the average price
        average_price = total_price / total_stocks

        # Pick stocks based on sector distribution
        picked_stocks = random.sample(stock_list, min(20, len(stock_list)))

        # Fetch stats for the picked stocks using multithreading
        stats_array = []
        for ticker in picked_stocks:
            stats_array.append(get_stats(ticker))

        # Sort the stats_array based on the absolute difference between each stock's price and the average_price
        sorted_stats = sorted(stats_array, key=lambda x: abs(x[1] - average_price))

        # Select the top 1 closest stock
        closest_stock = sorted_stats[0]

        # Initialize an empty array to store the information for the closest stock
        stock_info_array = []

        # Get information for the closest stock
        ticker, price = closest_stock
        sector = "Unknown"  # You can add logic to determine sector if needed
        stock_info_array.append([ticker, price, sector])

        # Return the array of arrays for the closest stock
        self.wfile.write(json.dumps(stock_info_array).encode('utf-8'))
        return
