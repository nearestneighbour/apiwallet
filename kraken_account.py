from account import account
import lib.krakenapi as ka

currencies = {'XXBT':'BTC','XETH':'ETH','ZEUR':'EUR','ZUSD':'USD','XLTC':'LTC','XXLM':'XLM'}

class kraken_account(account):
    def __init__(self, api_key=None, api_secret=None, file=None, data={}):
        super().__init__(data)
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                self.key = text[0].strip()
                self.secret = text[1].strip()
        else:
            self.key = api_key
            self.secret = api_secret

    def load_data(self):
        pairs = ''
        data = ka.api_query_private('Balance',{},self.key,self.secret)['result']
        for curr in data:
            if float(data[curr]) < 0.00002:
                continue
            if curr in currencies:
                self.balance[currencies[curr]] = float(data[curr])
            else:
                self.balance[curr] = float(data[curr])
            if (curr != 'ZEUR') and (curr != 'ZUSD') and (curr != 'XXBT'):
                if curr in currencies:
                    pairs += curr + 'XXBT,'
                else:
                    pairs += curr + 'XBT,'
        pairs += 'XXBTZEUR,XXBTZUSD'
        data = ka.api_query_public('Ticker',{'pair':pairs})['result']
        pairs = pairs.split(',')
        for p in pairs:
            if 'ZEUR' in p:
                self.btcprice['EUR'] = 1/float(data['XXBTZEUR']['c'][0])
            elif 'ZUSD' in p:
                self.btcprice['USD'] = 1/float(data['XXBTZUSD']['c'][0])
            elif p[:4] in currencies:
                self.btcprice[currencies[p[:4]]] = float(data[p]['c'][0])
            else:
                self.btcprice[p[:3]] = float(data[p]['c'][0])
        self.btc = 0
        for curr in self.balance:
            self.btc += self.balance[curr] * self.btcprice[curr]
