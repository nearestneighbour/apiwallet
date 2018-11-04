from account import account, updatable
from lib.bittrex import Bittrex

class bittrex_account(account):
    def __init__(self, api_key=None, api_secret=None, file=None, data={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        self.api = Bittrex(api_key, api_secret)
        super().__init__(data)
        self.u['price'] = updatable(self.load_btcpr, 60, False)

    def load_balance(self):
        bal = {}
        data = self.api.get_balances()['result']
        for curr in data:
            if curr['Balance'] < 0.00002:
                continue
            bal[curr['Currency']] = curr['Balance']
        return bal

    def value_self(self):
        v = {}
        bal = self.u['balance'].getdata()
        btcpr = self.u['price'].getdata()
        for curr in bal:
            v[curr] = bal[curr] * btcpr[curr]
        return v

    def value_base(self, base):
        if base == 'BTC':
            return self.value_self()
        return None

    def load_btcpr(self):
        b = {}
        for curr in self.u['balance'].getdata(False):
            if curr == 'BTC':
                b[curr] = 1.0
            else:
                data = self.api.get_ticker('BTC-'+curr)
                b[curr] = float(data['result']['Last'])
        return b
