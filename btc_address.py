from account import account
import requests

class btc_address(account):
    def __init__(self, pubkey=None, file=None, data={}):
        super().__init__(data)
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey

    def load_data(self):
        url = 'https://blockchain.info/q/addressbalance/' + self.pubkey
        self.balance['BTC'] = float(requests.get(url, timeout=10).text) / 100000000
        self.btc = self.balance['BTC']
