from account import account
from lib.bittrex import Bittrex

currencies = {'XXBT':'BTC','XETH':'ETH','ZEUR':'EUR','ZUSD':'USD','XLTC':'LTC','XXLM':'XLM'}

class bittrex_account(account):
    def __init__(self, api_key=None, api_secret=None, file=None, data={}):
        super().__init__(data)
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        self.api = Bittrex(api_key,api_secret)

    def load_data(self):
        self.btc = 0
        data = self.api.get_balances()['result']
        for curr in data:
            if curr['Balance'] < 0.00002:
                continue
            self.balance[curr['Currency']] = curr['Balance']
            if curr['Currency'] == 'BTC':
                self.btc += self.balance['BTC']
            else:
                self.btcprice[curr['Currency']] = self.get_btcpr(curr['Currency'])
                self.btc += self.balance[curr['Currency']] * self.btcprice[curr['Currency']]

    def get_btcpr(self, curr):
        return self.api.get_ticker('BTC-' + curr)['result']['Last']
