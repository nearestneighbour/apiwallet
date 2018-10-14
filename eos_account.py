from account import account
import requests

class eos_account(account):
    def __init__(self, accname, data={}):
        super().__init__(data)
        self.name = accname
        self.eosprice = {'NET':1,'CPU':1}

    def load_data(self):
        url = 'http://mainnet.eoscanada.com/v1/chain/get_account'
        param = '{"account_name":"' + self.name + '"}'
        data = requests.post(url,data=param).json()
        if 'core_liquid_balance' in data:
            self.balance['EOS'] = float(data['core_liquid_balance'][:-4])
        else:
            self.balance['EOS'] = 0
        self.balance['CPU'] = float(data['cpu_weight'])/10000
        self.balance['NET'] = float(data['net_weight'])/10000
        if data['refund_request'] != None:
            self.balance['EOS'] += float(data['refund_request']['cpu_amount'][:-4])
            self.balance['EOS'] += float(data['refund_request']['net_amount'][:-4])
        self.btcprice['EOS'] = self.get_eosbtc()
        self.balance['RAM'] = float(data['ram_quota'])-float(data['ram_usage'])
        self.eosprice['RAM'] = self.get_ramprice()
        for curr in self.eosprice:
            self.btcprice[curr] = self.btcprice['EOS'] * self.eosprice[curr]
        self.btcprice['RAM'] = self.eosprice['RAM'] * self.btcprice['EOS']
        self.eos = 0
        self.btc = 0
        for curr in self.eosprice:
            self.eos += self.balance[curr] * self.eosprice[curr]
            self.btc += self.balance[curr] * self.btcprice[curr]

    @staticmethod
    def get_eosbtc():
        url = 'https://api.kraken.com/0/public/Ticker?pair=eosxbt'
        return float(requests.get(url).json()['result']['EOSXBT']['c'][0])

    @staticmethod
    def get_ramprice():
        url = 'http://mainnet.eoscanada.com/v1/chain/get_table_rows'
        param = '{"scope":"eosio","code":"eosio","table":"rammarket","json":true}'
        data = requests.post(url,data=param).json()['rows'][0]
        return float(data['quote']['balance'][:-4]) / float(data['base']['balance'][:-4])
