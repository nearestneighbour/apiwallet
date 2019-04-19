import requests
from time import time

from .. import Account, Updatable

# To do: add token data

class eos_account(Account):
    def __init__(self, accname, **kwargs):
        # accname: name of EOS account
        self.name = accname
        super().__init__(corecurr = 'EOS', **kwargs)

    def load_balance(self):
        return self.load_data()

    def load_price(self):
        pr = self.load_price_data()[0]
        pr['BTC'] = 1/get_eosbtc()
        return pr

    def load_data(self):
        balance = self.load_core_balance()
        price, contract = self.load_price_data()
        balance.update(self.load_token_balance(price,contract))
        return balance

    def load_core_balance(self):
        # Load EOS balances (liquid, staked, delegated), RAM balance and RAM price
        url = 'http://mainnet.eoscanada.com/v1/chain/get_account'
        data = requests.post(url,data='{"account_name":"' + self.name + '"}').json()
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
        return bal

    def load_price_data(self):
        price = {'EOS':1.0, 'NET':1.0, 'CPU':1.0, 'DEL':1.0}
        # Load token prices
        contract = {}
        data = requests.get('https://api.newdex.io/v1/ticker/all').json()['data']
        for c in data:
            if c['contract'] == 'eosio.token':
                price['USD'] = 1/c['last']
                continue
            if c['symbol'][-3:] != 'eos':
                continue
            if c['volume'] > 1000: # Only include relevant (high volume) tokens
                price[c['currency']] = c['last']
                contract[c['currency']] = c['contract']
        # Load RAM price
        url = 'http://mainnet.eoscanada.com/v1/chain/get_table_rows'
        param = '{"scope":"eosio","code":"eosio","table":"rammarket","json":true}'
        data = requests.post(url, data=param).json()['rows'][0]
        price['RAM'] = float(data['quote']['balance'][:-4]) / float(data['base']['balance'][:-4])
        return price, contract

    def load_token_balance(self, prices, contracts):
        # Load token balances+prices
        bal = {}
        url = 'http://mainnet.eoscanada.com/v1/chain/get_currency_balance'
        for c in prices:
            if c in ['EOS','CPU','NET','DEL','RAM','USD','EUR']:
                continue
            param = '{"code":"'+contracts[c]+'","account":"'+self.name+'","symbol":"' + c + '"}'
            data = requests.post(url, data=param).json()
            if len(data) == 1:
                data = data[0][:data[0].find(' ')] # convert from e.g. '10.45 IQ' to '10.45'
                bal[c] = float(data)
        return bal

def get_eosbtc():
    # Get EOS/BTC price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=eosxbt'
    return float(requests.get(url).json()['result']['EOSXBT']['c'][0])
