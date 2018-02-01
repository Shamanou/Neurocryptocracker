#! /usr/bin/env python

import datetime
import json
import time

import requests
from pymongo import MongoClient


class Client(object):
    def __init__(self, url):
        self.url = url + "/api/2"
        self.session = requests.session()

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def get_ticker(self, symbol_code):
        return self.session.get("%s/public/ticker/%s" % (self.url, symbol_code)).json()


if __name__ == "__main__":
    mongoClient = MongoClient()
    tickers = mongoClient['hitbtc']['tickers']
    client = Client("https://api.hitbtc.com")
    current_time = datetime.datetime.now()
    days = 0
    bucket = 0
    symbols = client.get_symbol('')
    while days <= 30:
        for symbol in symbols:
            ticker = None
            symbol_id = symbol['id']
            while not ticker:
                try:
                    ticker = client.get_ticker(symbol_id)
                    ticker['bucket'] = bucket
                    tickers.insert_one(ticker)
                    del ticker['_id']
                    print "inserted " + json.dumps(ticker)
                    break
                except:
                    pass

        time.sleep(30)
        delta = current_time - datetime.datetime.now()
        days = delta.days
        bucket += 1
