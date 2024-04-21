from flask import Flask, jsonify, request
import yfinance as yf
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
from datetime import datetime
import numpy as np
import pandas as pd
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_sentiment():
    # Retrieve the stock ticker from the query parameters
    stock_ticker = request.args.get('ticker')
    
    stock = yf.Ticker(stock_ticker)
    chartData = stock.history(period='10950d', interval='1d')
    close_prices = chartData['Close']
    close_prices_list = close_prices.tolist()
    chartPointCt =  len(close_prices_list)

    try:
        news_articles = stock.news
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        news_articles = []
        
    GetStockInfo = yf.Ticker(stock_ticker)

    if 'longBusinessSummary' in GetStockInfo.info:
        long_business_summary = GetStockInfo.info['longBusinessSummary']
    else:
        print("No 'longBusinessSummary' found in the dictionary.")

    historical_data = stock.history(period='2d', interval='1d')
    yesterday_close = float(historical_data['Close'].iloc[-2])
    intraday_data = stock.history(period='1d', interval='1m')
    current_value = float(intraday_data['Close'].iloc[-1])

    # Calculate the change in dollars
    change_in_dollars = current_value - yesterday_close

    # Calculate the percent change
    percent_change = (change_in_dollars / yesterday_close) * 100

    # Get sentiment from news articles
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for article in news_articles:
        text = article['summary']
        sentiment_score = sia.polarity_scores(text)['compound']
        sentiment_scores.append(sentiment_score)

    # Calculate average sentiment score
    average_sentiment_score = np.mean(sentiment_scores)

    # Classify sentiment
    sentiment = 'Neutral'
    if average_sentiment_score > 0.05:
        sentiment = 'Positive'
    elif average_sentiment_score < -0.05:
        sentiment = 'Negative'

    # Prepare the response
    sentiment_info = {
        'Ticker': stock_ticker,
        'LongBusinessSummary': long_business_summary,
        'ChartData': close_prices_list,
        'ChartPointCount': chartPointCt,
        'CurrentPrice': current_value,
        'PriceChange': change_in_dollars,
        'PercentChange': percent_change,
        'Sentiment': sentiment,
        'AverageSentimentScore': average_sentiment_score
    }

    return jsonify(sentiment_info)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
