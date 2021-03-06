# This is a template class. All derived Account classes should follow this
# template in order to work with a Wallet instance as specified in wallet.py.

from .updatable import Updatable

class Account:
    def __init__(self, **kwargs):
        # kwargs:
        # # 'key'+'secret' or 'file' for exchange accounts (Kraken, Bittrex, Bitmex, ...)
        # # 'address' or 'file' for currency accounts (BTC, ETH, ...)
        # # 'core' for smart contract accounts (ETH, EOS, ...)
        if 'key' in kwargs:
            self.key = kwargs.pop('key')
            self.secret = kwargs.pop('secret', None)
        elif 'address' in kwargs:
            self.address = kwargs.pop('address')
        elif 'file' in kwargs:
            with open(kwargs.pop('file')) as f:
                text = f.readlines()
                for t in text:
                    var,val = t.strip().split(':')
                    exec("self." + var + " = '" + val + "'")
        self.core = kwargs.pop('core', None)
        self.meta = kwargs
        self.balancedata = Updatable(self.load_balance)
        self.pricedata = Updatable(self.load_price)

    @property
    def balance(self):
        b = self.balancedata()
        if self.core: # Only (not None) for smart contract accounts
            pr = self.pricedata()
            return {self.core: sum([b[c] * pr[c] for c in b])}
        return b

    @property
    def balance_ext(self):
        return self.balancedata()

    def balance_tocurr(self, curr='BTC'):
        pr = self.pricedata()
        if curr not in pr:
            raise NotImplementedError("Can't convert to currency " + curr)
        b = self.balance
        return {c: b[c] * pr[c] / pr[curr] for c in b}

    def load_balance(self):
        raise Exception("load_balance method not implemented")

    def load_price(self):
        if len(self.balance) == 1: # simple one-currency account
            (k,v), = self.balance.items()
            return {k: 1.0}
        else:
            raise Exception("Currency conversion not implemented")
