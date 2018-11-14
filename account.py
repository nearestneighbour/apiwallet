# Account Standard
# All account classes should comply to this standard in order to work with a
# Cryptopyfolio wallet object as specified in wallet.py. Account classes should
# be a child of the account class specified below.

# 3 types of accounts:
# - Single currency accounts (Bitmex*, BTCAddress, BTCXPUB, ETHAdress*)
# - Smart contract accounts (EOSAccount): tokens
# - Exchange accounts (Kraken, Bittrex): multiple currencies, what base?

from updatable import updatable

class account:
    def __init__(self, meta={}):
        self.meta = meta
        self.u = {'balance': updatable(self.load_balance)}
        # does this call account.load_balances or (child class).load_balances?

# BALANCE RELATED
    @property
    def balance(self):
        # Return dict of balances for account (see account specification)
        return self.u['balance'].data

    @property
    def balance_native(self):
        # Return balances converted to account primary currency
        # Default behaviour:
        b = self.balance
        if len(b) == 1:
            return b
        raise NotImplementedError('method value_self not implemented in child class')

    def balance_curr(self, curr):
        # Return balances converted to base currency
        # Default behaviour:
        b = self.balance
        if len(b) == 1 and curr in b:
            return b
        raise NotImplementedError('method value_base not implemented in child class')

# BALANCE DETAILS
    def currency(self, curr): # rename to currency_total
        # Return total balance of a particular currency (e.g. EOS+CPU+NET)
        # Default behaviour:
        b = self.balance
        if curr in b:
            return b[curr]
        else:
            return 0

# LOAD_BALANCE
    def load_balance(self):
        # Load balance data from API and update balances
        raise NotImplementedError('method load_balance not implemented in child class')
