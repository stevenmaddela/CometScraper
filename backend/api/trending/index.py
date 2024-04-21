from flask import Flask, Response, jsonify, request
import requests
import lxml.html

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    if path == "trending":
        return get_trending()
    else:
        return Response(
            "<h1>Flask</h1><p>Route not found: /%s</p>" % (path), mimetype="text/html"
        )

def get_trending():
    url_gainers = 'https://finance.yahoo.com/gainers'

    trendingArray = []
    ytext_gainers = requests.get(url_gainers).text
    yroot_gainers = lxml.html.fromstring(ytext_gainers)
    for x in yroot_gainers.xpath('//*[@id="fin-scr-res-table"]//a'):
        trendingArray.append(x.attrib['href'].split("/")[-1].split("?")[0])

    url_losers = 'https://finance.yahoo.com/losers'

    losingArray = []
    ytext_losers = requests.get(url_losers).text
    yroot_losers = lxml.html.fromstring(ytext_losers)
    for x in yroot_losers.xpath('//*[@id="fin-scr-res-table"]//a'):
        losingArray.append(x.attrib['href'].split("/")[-1].split("?")[0])

    # Prepare the HTML response
    html_response = "<h1>Trending and Losing Stocks</h1>"
    html_response += "<h2>Trending</h2>"
    html_response += "<ul>"
    for stock in trendingArray:
        html_response += f"<li>{stock}</li>"
    html_response += "</ul>"
    html_response += "<h2>Losing</h2>"
    html_response += "<ul>"
    for stock in losingArray:
        html_response += f"<li>{stock}</li>"
    html_response += "</ul>"

    return Response(html_response, mimetype="text/html")

if __name__ == '__main__':
    app.run(debug=True)
