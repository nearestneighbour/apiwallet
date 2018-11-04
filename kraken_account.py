from account import account, updatable
import lib.krakenapi as ka

# TO DO; choose self-base currency (EUR, USD, BTC, maybe ETH)

# Kraken gives weird names to currencies
currencies = {'XXBT':'BTC','XETH':'ETH','ZEUR':'EUR','ZUSD':'USD','XLTC':'LTC','XXLM':'XLM'}

class kraken_account(account):
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
        self.u['price'] = updatable(self.load_prices, 60, False)

    def value_self(self):
        return None

    def value_base(self, base):
        return None

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
        pr = {}
        pairs = ''
        for curr in self.u['balance'].getdata():
            if curr == 'EUR' or curr == 'USD':
                pairs += 'XBT' + curr + ','
            elif curr == 'BTC':
                pr[curr] = 1.0
            else:
                pairs += curr + 'XBT,'
        data = ka.api_query_public('Ticker',{'pair':pairs[:-1]})['result']
        for p in data:
            if len(p) == 6: # 'normal' trade pair
                pr[p[:3]] = float(data[p]['c'][0])
            elif p[1:4] == 'XBT': # XBTEUR or XBTUSD
                pr[p[5:]] = 1/float(data[p]['c'][0])
            else:
                pr[p[1:4]] = float(data[p]['c'][0])
        return pr