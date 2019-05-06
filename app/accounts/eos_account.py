import requests

from .. import Account, Updatable

corebalances = ['EOS','liquid','staked_CPU','staked_NET','delegated','refunding']

class eos_account(Account):
    def __init__(self, **kwargs):
        # kwargs: account (required)
        self.account = kwargs.pop('account')
        super().__init__(core = 'EOS', **kwargs)

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
        data = requests.post(url,data='{"account_name":"' + self.account + '"}').json()
        bal = {}
        if 'core_liquid_balance' in data:
            bal['liquid'] = float(data['core_liquid_balance'][:-4])
        cpu = float(data['total_resources']['cpu_weight'][:-4])
        net = float(data['total_resources']['net_weight'][:-4])
        dlg = data['voter_info']['staked'] / 10000 - (net+cpu)
        if dlg > 0:
            bal['staked_CPU'] = cpu
            bal['staked_NET'] = net
            bal['delegated'] = dlg
        if data['refund_request'] != None:
            bal['refunding'] = float(data['refund_request']['cpu_amount'][:-4])
            bal['refunding'] += float(data['refund_request']['net_amount'][:-4])
        # Load RAM balance
        bal['RAM'] = float(data['ram_quota'])-float(data['ram_usage'])
        return bal

    def load_price_data(self):
        price = {x: 1.0 for x in corebalances}
        #price = {'EOS':1,'liquid':1,'staked_CPU':1,'staked_NET':1,'delegated':1,'refunding':1}
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
            if c in corebalances + ['RAM','USD','EUR']:
                continue
            param = '{"code":"'+contracts[c]+'","account":"'+self.account+'","symbol":"'+c+'"}'
            data = requests.post(url, data=param).json()
            if len(data) == 1:
                data = data[0][:data[0].find(' ')] # convert from e.g. '10.45 IQ' to '10.45'
                bal[c] = float(data)
        return bal

def get_eosbtc():
    # Get EOS/BTC price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=eosxbt'
    return float(requests.get(url).json()['result']['EOSXBT']['c'][0])
