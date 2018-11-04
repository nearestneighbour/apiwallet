from account import account
import requests

apikey = '3ZW92AJRI8TDPPC47BCS81K7WXBG84ZE3T'

class eth_address(account):
    def __init__(self, pubkey=None, file=None, data={}):
        super().__init__(data)
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey
        self.u['ethbtc'] = updatable(get_ethbtc, 60, False)

    def load_balance(self):
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=' + self.pubkey + '&apikey=' + apikey
        bal = float(requests.get(url,timeout=15).json()['result'])/(10**18)
        return {'ETH': bal}

    def value_self(self):
        return self.u['balance'].getdata()

    def value_base(self, base):
        if base == 'ETH':
            return {'ETH': self.value_self() * self.u['ethbtc'].getdata()}
        return None

def get_ethbtc():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethxbt'
    return float(requests.get(url,timeout=15).json()['result']['XETHXXBT']['c'][0])
