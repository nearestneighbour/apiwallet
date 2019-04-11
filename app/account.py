# This is a template class. All derived Account classes should follow this
# template in order to work with a Wallet instance as specified in wallet.py.

# to do:
# add prices(self, curr=None)
# balance(None) -> return balance dict
# balance(curr) -> return balance float

from .updatable import Updatable

class Account:
    def __init__(self, meta={}):
        self.meta = meta
        self.native = None
        self.balancedata = Updatable(self.load_balance)
        self.pricedata = Updatable(self.load_prices)
        self.btcprice = Updatable(self.load_btcprice)

    def total_native(self): # right name? total worth of account in native currency
        b = self.balancedata()
        pr = self.pricedata()
        return sum([b[i]*pr[i] for i in b])

    def balance(self, curr=None):
        b = self.balancedata()
        if curr in b:
            return b[curr]
        elif curr == None:
            return b

    def balance_native(self, curr=None):
        b = self.balance(curr)
        pr = self.pricedata()
        bn = {}
        for c in b: # for every currency in balance
            bn[c] = b[c] * pr[c]
        return bn

    def balance_btc(self, curr=None):
        bn = self.balance_native(curr)
        pr = self.btcprice()
        bb = {}
        for c in bn: # for every currency in balance
            bb[c] = bn[c] * pr
        return bb

    def load_balance(self):
        # Load balance data from API and update balances
        raise NotImplementedError('method load_balance not implemented in child class')

    def load_prices(self):
        if self.native == None:
            raise NotImplementedError('`native` attribute not implemented in child class')
        if len(self.balancedata()) == 1 and self.native in self.balancedata():
            return {self.native: 1.0}
        else:
            raise NotImplementedError('method load_prices not implemented in child class')

    def load_btcprice(self):
        if self.native == 'BTC':
            return 1.0
        else:
            raise NotImplementedError('method load_btcprice not implemented in child class')
