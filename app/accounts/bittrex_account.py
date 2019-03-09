from .lib import bittrex
from .. import Account, Updatable

class bittrex_account(Account):
    def __init__(self, api_key=None, api_secret=None, file=None, meta={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        self.api = bittrex.Bittrex(api_key, api_secret)
        super().__init__(meta)
        self.native = 'BTC'
        self.btcprice = Updatable(self.load_btcprice)

    def load_balance(self):
        bal = {}
        data = self.api.get_balances()['result']
        for curr in data:
            if curr['Balance'] != None:
                if curr['Balance'] > 0.00002:
                    bal[curr['Currency']] = curr['Balance']
        return bal

    def load_prices(self):
        pr = {}
        for curr in self.balance():
            if curr == 'BTC':
                pr[curr] = 1.0
            else:
                data = self.api.get_ticker('BTC-'+curr)
                pr[curr] = float(data['result']['Last'])
        return pr
