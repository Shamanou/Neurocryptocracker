'''
Created on Oct 28, 2017

@author: Shamanou van Leeuwen
'''
import requests
from tgym.core import DataGenerator


class Generator(DataGenerator):
        
    @staticmethod
    def _generator(market):
        while True:
            y = requests.get("https://api.kraken.com/0/public/Ticker/BTC/"+market)
            if y.status_code == 200:
                y = y.json()
                yield float(y[u'bid']), float(y[u'ask'])
            
