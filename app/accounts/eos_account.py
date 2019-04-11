import requests
from time import time

from .. import Account, Updatable

# To do: add token data

class eos_account(Account):
    def __init__(self, accname, meta={}):
        # accname: name of EOS account
        self.name = accname
        self.native = 'EOS' # base currency
        super().__init__(meta)
        self.native = 'EOS'
        self.data_ext = Updatable(self.load_data_ext)

    def load_balance(self):
        # Load liquid/NET/CPU balance
        url = 'http://mainnet.eoscanada.com/v1/chain/get_account'
        param = '{"account_name":"' + self.name + '"}'
        data = requests.post(url,data=param).json()
        bal = {'EOS': 0, 'CPU': 0, 'NET': 0, 'DEL': 0}
        if 'core_liquid_balance' in data:
            bal['EOS'] = float(data['core_liquid_balance'][:-4]) # change 'EOS' to 'LIQ' oid?
        if data['self_delegated_bandwidth'] != None:
            bal['CPU'] = float(data['self_delegated_bandwidth']['cpu_weight'][:-4])
            bal['NET'] = float(data['self_delegated_bandwidth']['net_weight'][:-4])
            bal['DEL'] = data['voter_info']['staked'] / 10000
            bal['DEL'] -= (bal['CPU'] + bal['NET'])
        elif data['voter_info']['staked'] > 0:
            bal['DEL'] = data['voter_info']['staked'] / 10000
        if data['refund_request'] != None: # Add refunding EOS to staked EOS
            bal['CPU'] += float(data['refund_request']['cpu_amount'][:-4])
            bal['NET'] += float(data['refund_request']['net_amount'][:-4])
        # Load RAM balance
        bal['RAM'] = float(data['ram_quota'])-float(data['ram_usage'])
        # Load token balance
        pr, con = self.data_ext() # Load list of existing tokens
        balanceurl = 'http://mainnet.eoscanada.com/v1/chain/get_currency_balance'
        for c in pr: # iterate over tokens
            if c in ['EOS','CPU','NET','DEL','RAM']:
                continue
            param = '{"code":"'+con[c]+'","account":"'+self.name+'","symbol":"' + c + '"}'
            data = requests.post(balanceurl, data=param).json()
            if len(data) == 1:
                data = data[0][:data[0].find(' ')] # convert from e.g. '10.45 IQ' to '10.45'
                bal[c] = float(data)
        return bal

    def load_prices(self):
        return self.data_ext()[0]

    def load_data_ext(self):
        price = {}
        contract = {}
        # Load token prices
        priceurl = 'https://api.newdex.io/v1/ticker/all'
        pricedata = requests.get(priceurl).json()['data']
        for c in pricedata:
            if c['volume'] > 1000: # Only include relevant (i.e. high volume) tokens
                price[c['currency']] = c['last']
                contract[c['currency']] = c['contract']
        # Load RAM price
        ramurl = 'http://mainnet.eoscanada.com/v1/chain/get_table_rows'
        param = '{"scope":"eosio","code":"eosio","table":"rammarket","json":true}'
        ramdata = requests.post(ramurl, data=param).json()['rows'][0]
        price['RAM'] = float(ramdata['quote']['balance'][:-4]) / float(ramdata['base']['balance'][:-4])
        price['CPU'] = 1.0
        price['NET'] = 1.0
        price['EOS'] = 1.0
        price['DEL'] = 1.0
        return price, contract

    def load_btcprice(self):
        # Get EOS/BTC price from Kraken
        url = 'https://api.kraken.com/0/public/Ticker?pair=eosxbt'
        return float(requests.get(url).json()['result']['EOSXBT']['c'][0])
