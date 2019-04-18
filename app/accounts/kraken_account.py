import requests, json, urllib, time, hashlib, hmac, base64

from .. import Account, Updatable

# TO DO; choose native currency (EUR, USD, BTC, maybe ETH)

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
        self.native = ''
        self.prices = Updatable(self.load_prices)

    def load_balance(self):
        path = '/0/private/Balance'
        params = {'nonce': int(1000*time.time())}
        data = urllib.parse.urlencode(params)
        data = (str(params['nonce']) + data).encode()
        msg = path.encode() + hashlib.sha256(data).digest()
        sig = hmac.new(base64.b64decode(self.secret), msg, hashlib.sha512)
        sig = base64.b64encode(sig.digest())
        headers = {'API-Key': self.key, 'API-Sign': sig.decode()}
        url = 'https://api.kraken.com' + path
        data = requests.post(url, data=params, headers=headers, timeout=10).json()['result']
        bal = {}
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
        url = 'https://api.kraken.com/0/public/Ticker'
        params = {'pair': pairs[:-1]}
        data = requests.get(url, params=params, timeout=10).json()['result']
        for p in data:
            if len(p) == 6: # 'normal' trade pair
                pr[p[:3]] = float(data[p]['c'][0])
            elif p[1:4] == 'XBT': # XBTEUR or XBTUSD
                pr[p[5:]] = 1/float(data[p]['c'][0])
            else: # trade pair listed in 'currencies'
                pr[p[1:4]] = float(data[p]['c'][0])
        return pr
