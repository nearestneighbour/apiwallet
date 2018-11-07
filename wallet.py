from tabulate import tabulate
import requests
import json
import pickle
from updatable import updatable
# IDEAS
# add eth_xpub account type
# add open order functionality
# add wallet.balance to show other currencies in addition to BTC
#
# cryptopyfolio

class wallet:
    def __init__(self, *args):
        # Create new wallet object and add accounts
        # *args: account objects as specified by Account Standard
        self.base = 'BTC'
        self.accounts = []
        for acc in args:
            self.add_account(acc)
        self.u = {}
        self.u['btceur'] = updatable(load_btceur, 60, False) # See end of file for function declarations
        self.u['btcusd'] = updatable(load_btcusd, 60, False)

    def add_account(self, account):
        # Add account to wallet. If no add.data['name'] is specified, acc.data['name']
        # is set to a unique number. Accounts are then sorted by name.
        namedacc = [acc for acc in self.accounts if not acc.meta['name'].isdigit()]
        idacc = [acc for acc in self.accounts if acc.meta['name'].isdigit()]
        if 'name' not in account.meta:
            id = len(idacc)
            account.meta['name'] = str(id)
            self.accounts += [account]
        else:
            namedacc += [account]
            k = lambda x: x.meta['name'] # Sorting function
            self.accounts = sorted(namedacc, key=k)
            self.accounts += idacc

    def value_btc(self):
        # Get total BTC worth of accounts in wallet
        # Accounts are updated if outdated
        btc = 0
        for acc in self.accounts:
            try:
                a = acc.value_base('BTC')
            except NotImplementedError:
                raise NotImplementedError('Base BTC not implemented for acc '+acc.meta['name'])
            btc += sum([a[i] for i in a])
        return btc

    def value_eur(self):
        # Get total EUR worth of accounts in wallet
        return self.value_btc() * self.u['btceur'].getdata()

    def value_usd(self):
        # Get total USD worth of accounts in wallet
        return self.value_btc() * self.u['btcusd'].getdata()

    def currency_total(self, curr):
        tot = 0
        for acc in self.accounts:
            tot += acc.get_currency(curr)
        return tot

    def save(self, fname):
        # Save wallet object to file using pickle module
        # Does this store class functions as well? (i.e. does it not update with the code)
        with open(fname, 'wb') as f:
            pickle.dump(self, f)

    def show(self, what):
        return
        # Print overview of accounts in wallet. Print total BTC per account,
        # amount per currency per account, or amount per currency
        total = self.total_btc() # Update wallet
        if 'total' in what:
            eur = self.get_btceur()
            usd = self.get_btcusd()
            tot = 100/total
            table = []
            for acc in self.accounts:
                table.append([acc.meta['name'],acc.btc,acc.btc*eur,acc.btc*usd,acc.btc*tot])
            table.append(['Total value',self.btc,self.btc*eur,self.btc*usd,100])
            print('\n',tabulate(table,headers=['Account name','Total BTC',
            'Total EUR','Total USD','Percent']),'\n')
        if 'balance' in what:
            table = []
            for acc in self.accounts:
                j = True
                balances = acc.get_balances()
                values = acc.get_values()
                for curr in balances:
                    if j == True:
                        table.append([acc.meta['name'],curr,balances[curr],values[curr]])
                        j = False
                    else:
                        table.append(['',curr,balances[curr],values[curr]])
            print('\n',tabulate(table, headers=['Account','Currency','Balance','BTC']),'\n')
        if 'currency' in what:
            bal = {}
            pr = {}
            for acc in self.accounts:
                balances = acc.get_balances()
                values = acc.get_values()
                for curr in balances:
                    if curr not in bal:
                        val[curr] = values[curr]
                        bal[curr] = balances[curr]
                    else:
                        val[curr] += values[curr]
                        bal[curr] += balances[curr]
            table = []
            for curr in bal:
                table.append([curr,bal[curr],val[curr],100*val[curr]/total])
            print('\n',tabulate(table, headers=['Currency','Balance','BTC','Percent']),'\n')

    def __repr__(self):
        # Print wallet object
        return 'Wallet({})'.format(len(self.accounts))

    @staticmethod
    def show_account(account):
        pass

def load(fname):
    # Load wallet object from file using pickle module
    with open(fname, 'rb') as f:
        return pickle.load(f)

def load_btceur():
    # Get BTC/EUR price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbteur'
    return float(requests.get(url).json()['result']['XXBTZEUR']['c'][0])

def load_btcusd():
    # Get BTC/USD price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbtusd'
    return float(requests.get(url).json()['result']['XXBTZUSD']['c'][0])
