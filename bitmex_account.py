from account import account
from lib import bitmex

class bitmex_account(account):
    def __init__(self, api_key=None, api_secret=None, file=None, data={}):
        super().__init__(data)
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        self.api = bitmex.BitMEX(base_url='https://www.bitmex.com/api/v1/', apiKey=api_key, apiSecret=api_secret)

    def load_data(self):
        data = self.api._curl_bitmex(path='user/margin', verb='GET', timeout=10)
        self.balance['BTC'] = data['marginBalance'] / 100000000
        self.btc = self.balance['BTC']
