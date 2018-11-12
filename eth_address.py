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
        self.u['ethbtc'] = None


    def balance_curr(self, curr):
        if curr == 'BTC':
            if self.u['ethbtc'] == None:
                self.u['ethbtc'] = updatable(get_ethbtc, 60, False)
            return {'ETH':self.balance_native['ETH'] * self.u['ethbtc'].data}
        raise NotImplementedError('Currency '+curr+' not implemented in ETHACC')


    def load_balance(self):
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=' + self.pubkey + '&apikey=' + apikey
        bal = float(requests.get(url,timeout=15).json()['result'])/(10**18)
        return {'ETH': bal}

def get_ethbtc():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethxbt'
    return float(requests.get(url,timeout=15).json()['result']['XETHXXBT']['c'][0])
