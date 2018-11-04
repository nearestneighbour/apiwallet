from account import account, updatable
import requests

class btc_address(account):
    def __init__(self, pubkey=None, file=None, data={}):
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey
        super().__init__(data)

    def value_self(self):
        return self.u['balance'].getdata()

    def value_base(self, base):
        if base == 'BTC':
            return self.value_self()
        return None

    def load_balance(self):
        url = 'https://blockchain.info/q/addressbalance/' + self.pubkey
        return {'BTC': float(requests.get(url, timeout=10).text) / 100000000}