from flask import Flask, jsonify, request
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
import random
import os
import json
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_recommendations():
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

    def pick_stocks_based_on_distribution(sector_distribution, total_stocks=100, existing_stocks=[]):
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
    
    # Printing out the array of arrays received from the URL
    array_of_arrays_str = request.args.get('arrayOfArrays')
    FullStock_list = json.loads(array_of_arrays_str)
    print("Array of arrays received:", FullStock_list)

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

    # Select the top 8 closest stocks
    closest_stocks = sorted_stats[:8]

    end_time = time.time()
    print("Average price of each stock:", average_price)
    print(f"The program took {end_time - start_time:.2f} seconds.")
    print("Information for the closest stocks:")
    # Initialize an empty array to store the information for each stock
    stock_info_array = []

    # Iterate over each stock in closest_stocks
    for stock in closest_stocks:
        ticker, price = stock
        sector = sector_info.get(ticker, "Unknown")
        
        # Append the information for the current stock to the stock_info_array
        stock_info_array.append([ticker, price, sector])

    print(stock_info_array)

    # Return the array of arrays for the closest stocks
    return jsonify(stock_info_array)

if __name__ == '__main__':
    app.run(debug=True)
