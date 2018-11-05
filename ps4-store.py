# coding: utf-8
import requests
import json

not_names = ['Vollversion', 'Testversion']
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class game:
    def __init__(self, name, price, d_price, discount):
        self.name = name
        self.price = price
        self.d_price = d_price
        self.discount = discount
        self.index = 0

def by_price(item):
    return item.d_price

def get_games():
    start = 0
    params = {'game_content_type':'games',
             'platform':'ps4',
             'bucket':'games',
             'size':300,
             'start':start,
             'depth':1}
    url = 'https://store.playstation.com/valkyrie-api/de/DE/999/container/STORE-MSF75508-PRICEDROPSCHI'
    r = requests.get(url, params=params)
    if r.status_code == 200:
        print "Got the list of games!"
    j = json.loads(r.text)

    games = []
    for i in j['included']:
        if i['attributes']['name'] not in not_names :
            try:
                name = i['attributes']['name']
                discount = i['attributes']['skus'][0]['prices']['non-plus-user']['discount-percentage']
                price = i['attributes']['skus'][0]['prices']['non-plus-user']['strikethrough-price']['display']
                d_price = i['attributes']['skus'][0]['prices']['non-plus-user']['actual-price']['display']
                games.append(game(name, price, d_price, discount))
            except:
                pass


    games = sorted(games, key=by_price)
    return games

def main(event, context):
    games = get_games()

    html = '<html><head><meta charset="utf-8"></head><body>'

    table = '<table>'

    for g in games:
        row = '<tr>'
        row = row + '<td>' + g.name + '</td>'
        row = row + '<td>' + g.d_price + '</td>'
        row = row + '<td>' + g.price + '</td>'
        row = row + '<td>' + str(g.discount) + '</td>'
        row = row + '</tr>'
        table = table + row

    table = table + '</table>'

    html = html + table + '</body>'

    return html
