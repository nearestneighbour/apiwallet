# Account Standard
# All account classes should comply to this standard in order to work with a
# Cryptopyfolio wallet object as specified in wallet.py. Account classes should
# be a child of the account class specified below.

from updatable import updatable

class account:
    def __init__(self, meta={}):
        self.balance = {}
        self.meta = meta
        self.u = {'balance': updatable(self.load_balance, 60)}
        # does this call account.load_balances or (child class).load_balances?

    def get_balance(self):
        # Return dict of balances for account (see account specification)
        return self.u['balance'].getdata()

    def get_currency(self, curr):
        # Return total balance of a particular currency (e.g. EOS+CPU+NET)
        pass

    def load_balance(self):
        # Load balance data from API and update balances
        raise NotImplementedError('method load_balance not implemented in child class')

    def value_base(self, base):
        # Return balances converted to base currency
        raise NotImplementedError('method value_base not implemented in child class')

    def value_self(self):
        # Return balances converted to account primary currency
        raise NotImplementedError('method value_self not implemented in child class')

    def total_btc(self):
        # Return sum of balances (update account if outdated)

        # DEPRECATED
        raise DeprecationWarning('method total_btc is deprecated')

        if self.btc == None or self.get_age() > interval:
            self.load_data()
            self.updated = time()
        return self.btc

    def get_age(self):
        # Get time last account update

        # DEPRECATED
        raise DeprecationWarning('method get_age is deprecated')

        if self.updated == None:
            return -1
        else:
            return time()-self.updated
