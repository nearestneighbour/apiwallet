import requests

from .. import Account

class btc_address(Account):
    def load_balance(self):
        url = 'https://blockchain.info/q/addressbalance/' + self.address
        return {'BTC': float(requests.get(url, timeout=10).text) / 100000000}
