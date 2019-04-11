#
# Authentication code adapted from: github.com/BitMEX/easy-data-scripts
#

import requests, json, urllib, time, hashlib, hmac

from .. import Account

# To do: separate (un)realized profit, available margin etc

class bitmex_account(Account):
    def __init__(self, api_key=None, api_secret=None, file=None, testnet=False, meta={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                self.key = text[0].strip()
                self.secret = text[1].strip()
        else:
            self.key = api_key
            self.secret = api_secret
        if testnet:
            self.base_url = 'https://testnet.bitmex.com/api/v1'
        else:
            self.base_url = 'https://bitmex.com/api/v1/'
        super().__init__(meta)
        self.native = 'BTC'

    def load_balance(self):
        url = self.base_url + 'user/margin'
        auth = BitmexAuth(self.key, self.secret)
        data = requests.get(url, auth=auth, timeout=10).json()
        return {'BTC': data['marginBalance'] / 100000000}

class BitmexAuth(requests.auth.AuthBase):
    def __init__(self, api_key, api_secret):
        self.key = api_key
        self.secret = api_secret

    def __call__(self, r):
        nonce = str(int(round(time.time())+4))
        r.headers['api-expires'] = nonce
        r.headers['api-key'] = self.key
        sig = self.get_sig(self.secret, r.method, r.url, nonce, r.body)
        r.headers['api-signature'] = sig
        return r

    def get_sig(self, api_secret, verb, url, nonce, data):
        parsedURL = urllib.parse.urlparse(url)
        path = parsedURL.path
        if data == None:
            data = ''
        sec = bytes(api_secret, 'utf8')
        msg = bytes(verb + path + nonce + data, 'utf8')
        sig = hmac.new(sec, msg, digestmod=hashlib.sha256).hexdigest()
        return sig
