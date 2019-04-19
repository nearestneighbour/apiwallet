import requests

from .. import Account, Updatable

class eth_address(Account):
    def __init__(self, pubkey=None, file=None, **kwargs):
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey
        super().__init__(corecurr = 'ETH', **kwargs)

    def load_balance(self):
        return self.load_data()[0]

    def load_price(self):
        return self.load_data()[1]

    def load_data(self):
        url = 'http://api.ethplorer.io/getAddressInfo/' + self.pubkey + '?apiKey=freekey'
        data = requests.get(url,timeout=15).json()
        bal = {'ETH':data['ETH']['balance']} # ETH balance
        ethusd = get_ethusd()
        ethbtc = 1/get_ethbtc()
        pr = {'ETH':1.0, 'USD':1/ethusd, 'BTC': ethbtc}
        for t in data['tokens']:
            ti = t['tokenInfo']
            if ti['price'] == False: # no price data available; irrelevant token
                continue
            bal[ti['symbol']] = t['balance'] / (10**float(ti['decimals']))
            pr[ti['symbol']] = float(ti['price']['rate']) / ethusd
        return bal, pr

def get_ethbtc():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethxbt'
    return float(requests.get(url).json()['result']['XETHXXBT']['c'][0])

def get_ethusd():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethusd'
    return float(requests.get(url).json()['result']['XETHZUSD']['c'][0])
