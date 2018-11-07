from account import account
from updatable import updatable
import requests

apikey = '3ZW92AJRI8TDPPC47BCS81K7WXBG84ZE3T' # how to solve? (e.g. upload to Github)
# store in file like pubkey?

class eth_address(account):
    def __init__(self, pubkey=None, file=None, meta={}):
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey
        super().__init__(meta)
        self.u['ethbtc'] = updatable(get_ethbtc, 60, False)

    def value_base(self, base):
        if base == 'BTC':
            return {'ETH':self.value_self()['ETH'] * self.u['ethbtc'].getdata()}
        raise NotImplementedError('Currency '+base+' not implemented in ETHACC')

    def load_balance(self):
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=' + self.pubkey + '&apikey=' + apikey
        bal = float(requests.get(url,timeout=15).json()['result'])/(10**18)
        return {'ETH': bal}

def get_ethbtc():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethxbt'
    return float(requests.get(url,timeout=15).json()['result']['XETHXXBT']['c'][0])
