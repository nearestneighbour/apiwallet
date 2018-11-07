from account import account
from lib import bitmex

# To do: separate (un)realized profit, available margin etc?

class bitmex_account(account):
    def __init__(self, api_key=None, api_secret=None, file=None, meta={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        self.api = bitmex.BitMEX(base_url='https://www.bitmex.com/api/v1/', apiKey=api_key, apiSecret=api_secret)
        super().__init__(meta)

    def load_balance(self):
        data = self.api._curl_bitmex(path='user/margin', verb='GET', timeout=10)
        return {'BTC': data['marginBalance'] / 100000000}
