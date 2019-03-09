from .lib import kraken
from .. import Account, Updatable

# TO DO; choose self-base currency (EUR, USD, BTC, maybe ETH)

# Kraken gives weird names to currencies
currencies = {'XXBT':'BTC','XETH':'ETH','ZEUR':'EUR','ZUSD':'USD','XLTC':'LTC','XXLM':'XLM'}

class kraken_account(Account):
    def __init__(self, api_key=None, api_secret=None, file=None, meta={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                self.key = text[0].strip()
                self.secret = text[1].strip()
        else:
            self.key = api_key
            self.secret = api_secret
        super().__init__(meta)
        self.native = 'BTC'
        self.prices = Updatable(self.load_prices)

    def load_balance(self):
        bal = {}
        data = kraken.api_query_private('Balance',{},self.key,self.secret)['result']
        for curr in data:
            if float(data[curr]) < 0.00002:
                continue
            if curr in currencies:
                bal[currencies[curr]] = float(data[curr])
            else:
                bal[curr] = float(data[curr])
        return bal

    def load_prices(self):
        pr = {'BTC':1.0}
        pairs = 'XBTEUR,XBTUSD,'
        for curr in self.balance():
            if curr == 'EUR' or curr == 'USD' or curr == 'BTC':
                continue
            else:
                pairs += curr + 'XBT,'
        data = kraken.api_query_public('Ticker',{'pair':pairs[:-1]})['result']
        for p in data:
            if len(p) == 6: # 'normal' trade pair
                pr[p[:3]] = float(data[p]['c'][0])
            elif p[1:4] == 'XBT': # XBTEUR or XBTUSD
                pr[p[5:]] = 1/float(data[p]['c'][0])
            else: # trade pair listed in 'currencies'
                pr[p[1:4]] = float(data[p]['c'][0])
        return pr
