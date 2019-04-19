# This is a template class. All derived Account classes should follow this
# template in order to work with a Wallet instance as specified in wallet.py.

from .updatable import Updatable

class Account:
    def __init__(self, **kwargs):
        self.meta = kwargs
        self.balancedata = Updatable(self.load_balance)
        self.pricedata = Updatable(self.load_price)

    @property
    def balance(self):
        b = self.balancedata()
        if 'corecurr' in self.meta: # Only True for smart contract accounts
            pr = self.pricedata()
            bs = {self.meta['corecurr']: 0}
            for c in b:
                    bs[self.meta['corecurr']] += b[c] * pr[c]
            return bs
        return b

    @property
    def balance_ext(self):
        return self.balancedata()

    def balance_tocurr(self, curr='BTC'):
        b = self.balance
        pr = self.pricedata()
        if curr not in pr:
            raise Exception("Can't convert to currency " + curr)
        bc = {}
        for c in b:
            bc[c] = b[c] * pr[c] / pr[curr]
        return bc

    def load_balance(self):
        raise Exception("load_balance method not implemented")

    def load_price(self):
        if len(self.balance) == 1: # simple one-currency account
            (k,v), = self.balance.items()
            return {k: 1.0}
        else:
            raise Exception("Currency conversion not implemented")
