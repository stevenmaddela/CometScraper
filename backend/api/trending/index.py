from flask import Flask, jsonify, request
import requests
import lxml.html

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_trending():
    url = 'https://finance.yahoo.com/gainers'

    trendingArray = []
    ytext = requests.get(url).text
    yroot = lxml.html.fromstring(ytext)
    for x in yroot.xpath('//*[@id="fin-scr-res-table"]//a'):
        trendingArray.append(x.attrib['href'].split("/")[-1].split("?")[0])

    url2 = 'https://finance.yahoo.com/losers'

    losingArray = []
    ytext = requests.get(url2).text
    yroot = lxml.html.fromstring(ytext)
    for x in yroot.xpath('//*[@id="fin-scr-res-table"]//a'):
        losingArray.append(x.attrib['href'].split("/")[-1].split("?")[0])

    return jsonify({
        'Trending': trendingArray,
        'Losing': losingArray
    })

if __name__ == '__main__':
    app.run(debug=True)
