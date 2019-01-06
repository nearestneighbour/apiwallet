import requests

from account import Account
from updatable import Updatable

class eth_address(Account):
    def __init__(self, pubkey=None, file=None, meta={}):
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey
        super().__init__(meta)
        self.ethbtc = Updatable(get_ethbtc)


    @property
    def balance(self): # overwrite super().balance, see balance_extended()
        bal = self.balance_extended_native
        return {'ETH': sum([bal[c] for c in bal])}

    """ DEPRECATED
    def balance_curr(self, curr):
        if curr == 'ETH':
            return self.balance_native['ETH']
        elif curr == 'BTC':
            return {'ETH': self.balance_native['ETH'] * self.ethbtc()}
        raise NotImplementedError('Currency '+curr+' not implemented in ETHACC')
    """


    @property
    def balance_extended(self): # extended balance, separate ERC20 tokens
        return super().balance[1]

    @property
    def balance_extended_native(self):
        return super().balance[0]

    def load_balance(self):
        url = 'http://api.ethplorer.io/getAddressInfo/' + self.pubkey + '?apiKey=freekey'
        data = requests.get(url,timeout=15).json()
        bal = {'ETH':data['ETH']['balance']} # ETH balance
        ethusd = get_ethusd()
        tokenbal = bal # token balances (including ETH)
        tokeneth = {} # token balances denominated in ETH
        for t in data['tokens']:
            ti = t['tokenInfo']
            if ti['price'] == False:
                continue
            tokenbal[ti['symbol']] = t['balance'] / (10**float(ti['decimals']))
            tokenusd = tokenbal[ti['symbol']] * float(ti['price']['rate'])
            tokeneth[ti['symbol']] = tokenbal[ti['symbol']] / ethusd
        bal.update(tokeneth)
        return bal, tokenbal

def get_ethbtc():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethxbt'
    return float(requests.get(url).json()['result']['XETHXXBT']['c'][0])

def get_ethusd():
    url = 'https://api.kraken.com/0/public/Ticker?pair=ethusd'
    return float(requests.get(url).json()['result']['XETHZUSD']['c'][0])
