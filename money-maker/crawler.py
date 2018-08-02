import requests
from bs4 import BeautifulSoup
import config


def get_dollar_advice():
    investing = config.dollar['investing']
    url = investing['url']
    css = investing['css']
    header = investing['headers']

    source = requests.get(url=url, headers=header).text
    page = BeautifulSoup(source, 'html.parser')
    intervals = config.dollar['intervals']

    cols = {}
    for index, col in enumerate(page.select(css)[1:5]):
        cols[intervals[index]] = col.text
    return cols


def get_bank_dollar_price(bank_id):
    bank_config = config.dollar['banks'][bank_id]
    url = bank_config['url']
    buy_css = bank_config['buy_css']
    sell_css = bank_config['sell_css']
    name = bank_config['name']

    source = requests.get(url).text
    page = BeautifulSoup(source, 'html.parser')
    buy_price = page.select_one(buy_css).text[:7]
    sell_price = page.select_one(sell_css).text[:7]
    # print(name + ' - Buy:' + buy_price + ' / Sell:' + sell_price)

    return {
        'buy': float(buy_price.replace(',', '.')),
        'sell': float(sell_price.replace(',', '.')),
        'name': name
    }

