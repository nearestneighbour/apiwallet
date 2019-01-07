# This class does ...

import requests
import json
#import pickle --- see save/load functions

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

    """ include or not???
    def save(self, fname):
        # Save wallet object to file using pickle module
        # Does this store class functions as well? (i.e. does it not update with the code)
        with open(fname, 'wb') as f:
            pickle.dump(self, f)
    """

def load_btceur():
    # Get BTC/EUR price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbteur'
    return float(requests.get(url).json()['result']['XXBTZEUR']['c'][0])

def load_btcusd():
    # Get BTC/USD price from Kraken
    url = 'https://api.kraken.com/0/public/Ticker?pair=xbtusd'
    return float(requests.get(url).json()['result']['XXBTZUSD']['c'][0])

""" include or not??
def load(fname):
    # Load wallet object from file using pickle module
    with open(fname, 'rb') as f:
        return pickle.load(f)
"""
