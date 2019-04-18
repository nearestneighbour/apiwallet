import requests

from .. import Account

class btc_address(Account):
    def __init__(self, pubkey=None, file=None, **kwargs):
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey
        super().__init__(**kwargs)

    def load_balance(self):
        url = 'https://blockchain.info/q/addressbalance/' + self.pubkey
        return {'BTC': float(requests.get(url, timeout=10).text) / 100000000}
