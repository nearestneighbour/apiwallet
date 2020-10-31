import requests

from .. import Account

class ltc_address(Account):
    def load_balance(self):
        url = 'https://sochain.com/api/v2/get_address_balance/LTC/' + self.address
        data = requests.get(url, timeout=10).json()
        if 'data' not in data:
            raise TimeoutError("Could not load balance of LTC address")
        return {'LTC': float(data['data']['confirmed_balance'])}

    def load_price(self):
        ltcusd = get_ltcusd()
        ltcbtc = get_ltcbtc()
        return {'LTC': 1.0, 'USD': 1/ltcusd, 'BTC': 1/ltcbtc}

def get_ltcbtc():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ltcxbt'
    return float(requests.get(url).json()['result']['XLTCXXBT']['c'][0])

def get_ltcusd():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ltcusd'
    return float(requests.get(url).json()['result']['XLTCZUSD']['c'][0])
