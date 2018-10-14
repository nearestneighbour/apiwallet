from tabulate import tabulate
import requests
# TO DO
# add eth_xpub account type
# add open order functionality
# add wallet.balance to show other currencies in addition to BTC

class wallet():
    def __init__(self, *args):
        self.btc = 0
        self.accounts = []
        for acc in args:
            self.add_account(acc)

    def add_account(self, acc):
        self.accounts.append(acc)
        self.btc = None

    def find_account(self, keyword, value):
        d = [acc for acc in self.accounts if keyword in acc.data]
        return [acc for acc in d if acc.data[keyword]==value]

    def total_btc(self):
        self.btc = 0
        for acc in self.accounts:
            self.btc += acc.total_btc()
        return self.btc

    def total_eur(self):
        return self.get_btceur() * self.total_btc()

    def total_usd(self):
        return self.get_btcusd() * self.total_btc()

    def show(self):
        eur = self.get_btceur()
        usd = self.get_btcusd()
        tot = 100/self.total_btc()
        id = 0
        table = []
        for acc in self.accounts:
            if 'name' in acc.data:
                name = acc.data['name']
            else:
                name = id
            table.append([name,acc.btc,acc.btc*eur,acc.btc*usd,acc.btc*tot])
            id += 1
        table.append(['Total value',self.btc,self.btc*eur,self.btc*usd,100])
        print(tabulate(table, headers=['Account name','Total BTC','Total EUR','Total USD','Percent']))
        id = 0
        table = []
        for acc in self.accounts:
            if 'name' in acc.data:
                name = acc.data['name']
            else:
                name = id
            balances,prices = acc.get_balances()
            for curr in balances:
                table.append([name,curr,balances[curr],balances[curr]*prices[curr]])
            id += 1
        print('\n',tabulate(table, headers=['Account','Currency','Balance','BTC']))

    @staticmethod
    def get_btceur():
        url = 'https://api.kraken.com/0/public/Ticker?pair=xbteur'
        return float(requests.get(url).json()['result']['XXBTZEUR']['c'][0])

    @staticmethod
    def get_btcusd():
        url = 'https://api.kraken.com/0/public/Ticker?pair=xbtusd'
        return float(requests.get(url).json()['result']['XXBTZUSD']['c'][0])
