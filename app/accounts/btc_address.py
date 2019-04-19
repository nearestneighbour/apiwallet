import requests

from .. import Account

class btc_address(Account):
    def __init__(self, **kwargs):
        # kwargs: pubkey=None, file=None
        if 'pubkey' not in kwargs:
            with open(kwargs.pop('file')) as f:
                kwargs['pubkey'] = f.readlines()[0].strip()
        self.pubkey = kwargs.pop('pubkey')
        super().__init__(**kwargs)

    def load_balance(self):
        url = 'https://blockchain.info/q/addressbalance/' + self.pubkey
        return {'BTC': float(requests.get(url, timeout=10).text) / 100000000}
