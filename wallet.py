# This class does ...

from tabulate import tabulate
import requests
import json
import pickle

from updatable import Updatable

class Wallet:
    def __init__(self, *args):
        # Create new wallet object and add accounts
        # *args: account objects as specified by Account Standard
        self.base = 'BTC'
        self.accounts = []
        for acc in args:
            self.add_account(acc)
        self.pr = {'EUR':Updatable(load_btceur, 60),'USD':Updatable(load_btcusd, 60)}

    def add_account(self, account):
        # Add account to wallet. If no account.data['name'] is specified, account.data['name']
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


    def total_btc(self):
        btc = 0
        for acc in self.accounts:
            btc += acc.total_native() * acc.btcprice()
        return btc

    def total_curr(self, curr=None):
        # Get total worth of accounts in curr, e.g. 'USD' or 'EUR'
        return self.total_btc() * self.pr[curr]()

    def balance(self, curr=None):
        balance = {}
        for acc in self.accounts:
            bal = acc.balance(curr)
            for b in bal:
                if b not in balance:
                    balance[b] = bal[b]
                else:
                    balance[b] += bal[b]
        return balance

    def balance_btc(self, curr=None):
        balance = {}
        for acc in self.accounts:
            bal = acc.balance_btc(curr)
            for b in bal:
                if b not in balance:
                    balance[b] = bal[b]
                else:
                    balance[b] += bal[b]
        return balance

    def save(self, fname):
        # Save wallet object to file using pickle module
        # Does this store class functions as well? (i.e. does it not update with the code)
        with open(fname, 'wb') as f:
            pickle.dump(self, f)

    def __repr__(self):
        # Print wallet object
        return 'Wallet({})'.format(len(self.accounts))

    # DEPRECATED
    def show(self, what):
        return
        # Print overview of accounts in wallet. Print total BTC per account,
        # amount per currency per account, or amount per currency
        total = self.total_btc # Update wallet
        if 'total' in what:
            eur = self.get_btceur
            usd = self.get_btcusd
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
