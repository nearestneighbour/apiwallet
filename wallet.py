from tabulate import tabulate
import requests
import json
import pickle
# TO DO
# add eth_xpub account type
# add open order functionality
# add wallet.balance to show other currencies in addition to BTC
# link to telegram
#
# cryptopyfolio

class wallet():
    def __init__(self, *args):
        # Create new wallet object and add accounts
        # *args: account objects as specified by Account Standard
        self.btc = 0
        self.accounts = []
        for acc in args:
            self.add_account(acc)

    def add_account(self, account):
        # Add account to wallet. If no add.data['name'] is specified, acc.data['name']
        # is set to a unique number. Accounts are then sorted by name.
        namedacc = [acc for acc in self.accounts if not acc.data['name'].isdigit()]
        idacc = [acc for acc in self.accounts if acc.data['name'].isdigit()]
        if 'name' not in account.data:
            id = len(idacc)
            account.data['name'] = str(id)
            self.accounts += [account]
        else:
            namedacc += [account]
            k = lambda x: x.data['name'] # Sorting function
            self.accounts = sorted(namedacc, key=k)
            self.accounts += idacc
        self.btc = None

    def total_btc(self):
        # Get total BTC worth of accounts in wallet
        # Accounts are updated if outdated
        self.btc = 0
        for acc in self.accounts:
            self.btc += acc.total_btc()
        return self.btc

    def total_eur(self):
        # Get total EUR worth of accounts in wallet
        return self.get_btceur() * self.total_btc()

    def total_usd(self):
        # Get total USD worth of accounts in wallet
        return self.get_btcusd() * self.total_btc()

    def save(self, fname):
        # Save wallet object to file using pickle module
        with open(fname, 'wb') as f:
            pickle.dump(self, f)

    def find_account(self, keyword, value):
        # Find account in wallet by matching keyword in account.data to value
        d = [acc for acc in self if keyword in acc.data]
        return [acc for acc in d if acc.data[keyword]==value]

    def get_age(self):
        # Return time in seconds since updating wallet balances
        ages = [acc.get_age() for acc in self.accounts]
        return max(floor(ages))

    def show(self, what):
        # Print overview of accounts in wallet. Print total BTC per account,
        # amount per currency per account, or amount per currency
        total = self.total_btc() # Update wallet
        if 'total' in what:
            eur = self.get_btceur()
            usd = self.get_btcusd()
            tot = 100/total
            table = []
            for acc in self.accounts:
                table.append([acc.data['name'],acc.btc,acc.btc*eur,acc.btc*usd,acc.btc*tot])
            table.append(['Total value',self.btc,self.btc*eur,self.btc*usd,100])
            print('\n',tabulate(table,headers=['Account name','Total BTC',
            'Total EUR','Total USD','Percent']),'\n')
        if 'balance' in what:
            table = []
            for acc in self.accounts:
                j = True
                balances,prices = acc.get_balances()
                for curr in balances:
                    if j == True:
                        table.append([acc.data['name'],curr,balances[curr],balances[curr]*prices[curr]])
                        j = False
                    else:
                        table.append(['',curr,balances[curr],balances[curr]*prices[curr]])
            print('\n',tabulate(table, headers=['Account','Currency','Balance','BTC']),'\n')
        if 'currency' in what:
            bal = {}
            pr = {}
            for acc in self.accounts:
                balances, prices = acc.get_balances()
                for curr in balances:
                    if curr not in pr:
                        pr[curr] = prices[curr]
                    if curr not in bal:
                        bal[curr] = balances[curr]
                    else:
                        bal[curr] += balances[curr]
            table = []
            for curr in bal:
                table.append([curr,bal[curr],bal[curr]*pr[curr],100*bal[curr]*pr[curr]/total])
            print('\n',tabulate(table, headers=['Currency','Balance','BTC','Percent']),'\n')

    def __repr__(self):
        # Print wallet object
        return 'Wallet({})'.format(len(self.accounts))

    @staticmethod
    def load(fname):
        # Load wallet object from file using pickle module
        with open(fname, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def get_btceur():
        # Get BTC/EUR price from Kraken
        url = 'https://api.kraken.com/0/public/Ticker?pair=xbteur'
        return float(requests.get(url).json()['result']['XXBTZEUR']['c'][0])

    @staticmethod
    def get_btcusd():
        # Get BTC/USD price from Kraken
        url = 'https://api.kraken.com/0/public/Ticker?pair=xbtusd'
        return float(requests.get(url).json()['result']['XXBTZUSD']['c'][0])
