from account import account, updatable
from lib import bitmex

# To do: separate (un)realized profit, available margin etc?

class bitmex_account(account):
    def __init__(self, api_key=None, api_secret=None, file=None, data={}):
        if api_key == None:
            with open(file) as f:
                text = f.readlines()
                api_key = text[0].strip()
                api_secret = text[1].strip()
        self.api = bitmex.BitMEX(base_url='https://www.bitmex.com/api/v1/', apiKey=api_key, apiSecret=api_secret)
        super().__init__(data)

    def value_self(self):
        return self.u['balance'].getdata()

    def value_base(self, base):
        if base == 'BTC':
            return self.value_self()
        return None

    def load_balance(self):
        data = self.api._curl_bitmex(path='user/margin', verb='GET', timeout=10)
        return {'BTC': data['marginBalance'] / 100000000}