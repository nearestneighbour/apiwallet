from .lib import bitmex
from app import Account

# To do: separate (un)realized profit, available margin etc

class bitmex_account(Account):
    def __init__(self, api_key=None, api_secret=None, file=None, testnet=False, meta={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        if testnet == True:
            url = 'https://testnet.bitmex.com/api/v1'
        else:
            url = 'https://bitmex.com/api/v1/'
        self.api = bitmex.BitMEX(base_url=url, apiKey=api_key, apiSecret=api_secret)
        super().__init__(meta)
        self.native = 'BTC'

    def load_balance(self):
        data = self.api._curl_bitmex(path='user/margin', verb='GET', timeout=10)
        return {'BTC': data['marginBalance'] / 100000000}
