# This class does ...

import requests

from .updatable import Updatable

class Wallet:
    def __init__(self, *args, **kwargs):
        # Create new wallet object and add accounts
        # *args: account objects as specified by Account Standard
        # kwargs: meta-info about wallet
        self.accounts = list(args)
        self.meta = kwargs
        self.btcprice = {'EUR':Updatable(get_btceur, 60),'USD':Updatable(get_btcusd, 60)}

    @property
    def balance(self):
        b = {}
        for acc in self.accounts:
            subb = acc.balance
            for c in subb:
                b[c] = subb[c] + (b[c] if c in b else 0)
        return b

    @property
    def balance_ext(self):
        b = {}
        for acc in self.accounts:
            subb = acc.balance_ext
            for c in subb:
                b[c] = subb[c] + (b[c] if c in b else 0)
        return b

    def balance_tocurr(self, curr='BTC'):
        b = {}
        for acc in self.accounts:
            subb = acc.balance_tocurr(curr)
            for c in subb:
                b[c] = subb[c] + (b[c] if c in b else 0)
        return b

    def filter_balance(self, b, thr=0):
        return {c:b[c] for c in b if b[c]>=thr}

    def total(self, curr='BTC'):
        try:
            b = self.balance_tocurr(curr)
        except NotImplementedError:
            if curr in self.btcprice:
                b = self.balance_tocurr('BTC')
                b = {c:b[c]*self.btcprice[curr]() for c in b}
        return sum([b[c] for c in b])

def get_btceur():
    # Get BTC/EUR price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbteur'
    return float(requests.get(url).json()['result']['XXBTZEUR']['c'][0])

def get_btcusd():
    # Get BTC/USD price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbtusd'
    return float(requests.get(url).json()['result']['XXBTZUSD']['c'][0])
