from account import Account
from updatable import Updatable
import lib.krakenapi as ka

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
        self.u['price'] = Updatable(self.load_prices)


    @property
    def balance_native(self): # base curr: BTC
        v = {}
        bal = self.balance
        pr = self.u['price'].data
        for c in bal:
            v[c] = bal[c] * pr[c]
        return v

    def balance_curr(self, curr):
        if curr == 'BTC':
            return self.balance_native
        elif curr == 'EUR':
            basepr = 1 / self.u['price'].data['EUR']
        elif curr == 'USD':
            basepr = 1 / self.u['price'].data['USD']
        else:
            raise NotImplementedError('Currency '+curr+' not implemented in KRAKEN')
        bal = self.balance_native
        for c in bal:
            bal[c] = bal[c] * basepr
        return bal


    def load_balance(self):
        bal = {}
        data = ka.api_query_private('Balance',{},self.key,self.secret)['result']
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
        for curr in self.balance:
            if curr == 'EUR' or curr == 'USD' or curr == 'BTC':
                continue
            else:
                pairs += curr + 'XBT,'
        data = ka.api_query_public('Ticker',{'pair':pairs[:-1]})['result']
        for p in data:
            if len(p) == 6: # 'normal' trade pair
                pr[p[:3]] = float(data[p]['c'][0])
            elif p[1:4] == 'XBT': # XBTEUR or XBTUSD
                pr[p[5:]] = 1/float(data[p]['c'][0])
            else: # trade pair listed in 'currencies'
                pr[p[1:4]] = float(data[p]['c'][0])
        return pr
