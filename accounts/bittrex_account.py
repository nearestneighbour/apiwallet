from .lib import bittrex
from account import Account
from updatable import Updatable

class bittrex_account(Account):
    def __init__(self, api_key=None, api_secret=None, file=None, meta={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        self.api = bittrex.Bittrex(api_key, api_secret)
        super().__init__(meta)
        self.price = Updatable(self.load_btcpr)


    @property
    def balance_native(self):
        v = {}
        bal = self.balance
        btcpr = self.price()
        for curr in bal:
            v[curr] = bal[curr] * btcpr[curr]
        return v

    def balance_curr(self, curr):
        if curr == 'BTC':
            return self.balance_native
        raise NotImplementedError('Currency '+curr+' not implemented in BITTREX')


    def load_balance(self):
        bal = {}
        data = self.api.get_balances()['result']
        for curr in data:
            if curr['Balance'] > 0.00002:
                bal[curr['Currency']] = curr['Balance']
        return bal

    def load_btcpr(self):
        b = {}
        for curr in self.balance:
            if curr == 'BTC':
                b[curr] = 1.0
            else:
                data = self.api.get_ticker('BTC-'+curr)
                b[curr] = float(data['result']['Last'])
        return b
