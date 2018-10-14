class account():
    def __init__(self, data={}):
        self.balance = {}
        self.btcprice = {'BTC':1}
        self.btc = None
        self.data = data

    def load_data(self):
        raise NotImplementedError('method load_data not implemented in child class')

    def total_btc(self):
        if self.btc == None:
            self.load_data()
        return self.btc

    def get_balances(self):
        return self.balance, self.btcprice
