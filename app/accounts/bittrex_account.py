import requests, urllib, time, hashlib, hmac

from .. import Account, Updatable

class bittrex_account(Account):
    def __init__(self, **kwargs):
        # kwargs: api_key=None, api_secret=None, file=None
        if 'api_key' not in kwargs:
            with open(kwargs.pop('file')) as f:
                text = f.readlines()
                self.key = text[0].strip()
                self.secret = text[1].strip()
        else:
            self.key = kwargs.pop('api_key')
            self.secret = kwargs.pop('api_secret')
        super().__init__(**kwargs)

    def load_balance(self):
        url =  'https://bittrex.com/api/v1.1/account/getbalances'
        nonce = str(int(time.time() * 1000))
        url += '?apikey={0}&nonce={1}&'.format(self.key, nonce)
        sig = hmac.new(self.secret.encode(), url.encode(), hashlib.sha512).hexdigest()
        data = requests.get(url, headers={"apisign": sig}).json()['result']
        bal = {}
        for curr in data:
            if curr['Balance'] != None:
                if curr['Balance'] > 0.00002:
                    bal[curr['Currency']] = curr['Balance']
        return bal

    def load_price(self):
        url =  'https://bittrex.com/api/v1.1/public/getmarketsummaries'
        data = requests.get(url).json()['result']
        bal = self.balance
        pr = {}
        for market in data:
            if market['MarketName'][:4] == 'BTC-':
                curr = market['MarketName'][4:]
                if curr in bal:
                    pr[curr] = market['Last']
        pr['BTC'] = 1
        return pr
