from time import time

# Account Standard
# All account classes should comply to this standard in order to work with a
# Cryptopyfolio wallet object as specified in wallet.py. Account classes should
# be a child of the account class specified below.

interval = 60

class account():
    def __init__(self, data={}):
        self.balance = {}
        self.btcprice = {'BTC':1}
        self.btc = None
        self.data = data
        self.updated = None

    def load_data(self):
        # Load balance data from API and update balances
        raise NotImplementedError('method load_data not implemented in child class')

    def total_btc(self):
        # Return sum of balances (update account if outdated)
        if self.btc == None or self.get_age() > interval:
            self.load_data()
            self.updated = time()
        return self.btc

    def get_balances(self):
        # Return array of balances for account
        # To do: update account if outdated
        return self.balance, self.btcprice

    def get_age(self):
        # Get time last account update
        if self.updated == None:
            return -1
        else:
            return time()-self.updated
