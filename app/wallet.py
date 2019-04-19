# This class does ...

import requests
import pandas as pd

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
            # First check if account can convert, otherwise try self
            try:
                subb = acc.balance_tocurr(curr)
            except NotImplementedError:
                if curr in self.btcprice:
                    subb = acc.balance_tocurr()
                    subb = {c:subb[c]*self.btcprice[curr]() for c in subb}
            except:
                raise NotImplementedError("Can't convert to currency " + curr)
            for c in subb:
                b[c] = subb[c] + (b[c] if c in b else 0)
        return b

    def filter_balance(self, b, thr=0):
        return {c:b[c] for c in b if b[c]>=thr}

    def total(self, curr='BTC'):
        b = self.balance_tocurr(curr)
        return sum([b[c] for c in b])

    def to_dataframe(self, curr=['','BTC','EUR']):
        df = pd.DataFrame()
        for c in curr:
            if c == '':
                b = self.balance
            else:
                b = self.balance_tocurr(c)
            df[c] = pd.Series(b)
        return df

def get_btceur():
    # Get BTC/EUR price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbteur'
    return float(requests.get(url).json()['result']['XXBTZEUR']['c'][0])

def get_btcusd():
    # Get BTC/USD price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbtusd'
    return float(requests.get(url).json()['result']['XXBTZUSD']['c'][0])
