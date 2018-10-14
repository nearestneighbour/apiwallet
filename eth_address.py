from account import account
import requests

apikey = '3ZW92AJRI8TDPPC47BCS81K7WXBG84ZE3T'

class eth_address(account):
    def __init__(self, pubkey=None, file=None, data={}):
        super().__init__(data)
        if pubkey == None:
            with open(file) as f:
                pubkey = f.readlines()[0].strip()
        self.pubkey = pubkey
        self.balance['ETH'] = 0

    def load_data(self):
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=' + self.pubkey + '&apikey=' + apikey
        self.balance['ETH'] = float(requests.get(url,timeout=15).json()['result'])/(10**18)
        self.btcprice['ETH'] = self.get_ethbtc()
        self.btc = self.balance['ETH'] * self.btcprice['ETH']

    @staticmethod
    def get_ethbtc():
        url = 'https://api.kraken.com/0/public/Ticker?pair=ethxbt'
        return float(requests.get(url,timeout=15).json()['result']['XETHXXBT']['c'][0])
