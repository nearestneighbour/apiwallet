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
        self.u['tokens'] = updatable(self.load_tokenbalance) # data[0]: balances, data[1] balances in ETH
        self.u['ethbtc'] = updatable(get_ethbtc)


    @property
    def balance(self): # overwrite super().balance, see balance_ext(self)
        bal = self.balance_extended_native
        return {'ETH': sum([bal[c] for c in bal])}

    def balance_curr(self, curr):
        if curr == 'ETH':
            return self.balance_native['ETH']
        elif curr == 'BTC':
            return {'ETH': self.balance_native['ETH'] * self.u['ethbtc'].data}
        raise NotImplementedError('Currency '+curr+' not implemented in ETHACC')


    @property
    def balance_extended(self): # extended balance, separate ERC20 tokens
        return super().balance

    @property
    def balance_extended_native(self):
        v = {'ETH': self.balance_extended['ETH']}
        v.update(self.u['tokens'].data[1]) # add tokens
        return v

    def load_balance(self):
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=' + self.pubkey + '&apikey=' + apikey
        bal = {'ETH':float(requests.get(url,timeout=15).json()['result'])/(10**18)}
        bal.update(self.u['tokens'].data[0]) # add token balances
        return bal

    def load_tokenbalance(self):
        url = 'http://api.ethplorer.io/getAddressInfo/' + self.pubkey + '?apiKey=freekey'
        data = requests.get(url).json()['tokens']
        ethusd = get_ethusd()
        bal = {}
        native = {}
        for t in data:
            ti = t['tokenInfo']
            if t['tokenInfo']['price'] == False:
                continue
            bal[ti['symbol']] = t['balance'] / (10**float(ti['decimals']))
            usdbal = bal[ti['symbol']] * float(ti['price']['rate'])
            native[ti['symbol']] = usdbal / ethusd
        return bal, native

def get_ethbtc():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethxbt'
    return float(requests.get(url).json()['result']['XETHXXBT']['c'][0])

def get_ethusd():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethusd'
    return float(requests.get(url).json()['result']['XETHZUSD']['c'][0])
