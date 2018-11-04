from account import account, updatable
import requests
from time import time

# To do: add token data

class eos_account(account):
    def __init__(self, accname, meta={}):
        # accname: name of EOS account
        self.name = accname
        super().__init__(meta)
        self.u['eosbtc'] = updatable(load_eosbtc, 30, False) # See end of file for function declarations
        self.u['eoseth'] = updatable(load_eoseth, 30, False)
        self.u['rampr'] = updatable(load_ramprice, 30)

    def value_self(self):
        v = {}
        bal = self.u['balance'].getdata()
        for c in ['EOS','CPU','NET']:
            v[c] = bal[c]
        v['RAM'] = bal['RAM'] * self.u['rampr'].getdata()
        return v

    def value_base(self, base):
        if base == 'BTC':
            basepr = self.u['eosbtc'].getdata()
        elif base == 'ETH':
            basepr = self.u['eoseth'].getdata()
        else:
            return None # raise error
        v1 = self.value_self()
        v2 = {}
        for curr in v1:
            v2[curr] = v1[curr] * basepr
        return v2

    def load_balance(self):
        url = 'http://mainnet.eoscanada.com/v1/chain/get_account'
        param = '{"account_name":"' + self.name + '"}'
        data = requests.post(url,data=param).json()
        bal = {}
        if 'core_liquid_balance' in data:
            bal['EOS'] = float(data['core_liquid_balance'][:-4]) # change 'EOS' to 'LIQ' oid?
        else:
            bal['EOS'] = 0
        bal['CPU'] = float(data['cpu_weight'])/10000
        bal['NET'] = float(data['net_weight'])/10000
        # Add refunding EOS to staked EOS
        if data['refund_request'] != None:
            bal['CPU'] += float(data['refund_request']['cpu_amount'][:-4])
            bal['NET'] += float(data['refund_request']['net_amount'][:-4])
        # Get available RAM in bytes
        bal['RAM'] = float(data['ram_quota'])-float(data['ram_usage'])
        return bal

    def get_currency(self, curr):
        # idea: if curr==(CPU or NET), return bytes/seconds
        if curr == 'EOS':
            data = self.value_self()
            return sum([data[c] for c in data])
        elif curr == 'RAM':
            return self.u['balance'].getdata()['RAM']

def load_eosbtc():
    # Get EOS/BTC price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=eosxbt'
    return float(requests.get(url).json()['result']['EOSXBT']['c'][0])

# REDUNDANT? (IMPLEMENT IN WALLET.PY INSTEAD?)
def load_eoseth():
    # Get EOS/ETH price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=eoseth'
    return float(requests.get(url).json()['result']['EOSETH']['c'][0])

def load_ramprice():
    # Get RAM price in BYTE/EOS
    url = 'http://mainnet.eoscanada.com/v1/chain/get_table_rows'
    param = '{"scope":"eosio","code":"eosio","table":"rammarket","json":true}'
    data = requests.post(url,data=param).json()['rows'][0]
    return float(data['quote']['balance'][:-4]) / float(data['base']['balance'][:-4])
