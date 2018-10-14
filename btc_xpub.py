from account import account
import requests
from btcpy.setup import setup
from btcpy.structs.hd import ExtendedPublicKey
from btcpy.structs.address import P2shAddress, P2wpkhAddress

setup('mainnet')

class btc_xpub(account):
    def __init__(self, xpub=None, file=None, address='nested', data={}):
        super().__init__(data)
        if xpub == None:
            with open(file) as f:
                xpub = f.readlines()[0].strip()
        self.xpub = ExtendedPublicKey.decode(xpub)
        self.address = address
        self.last_spend = -1
        self.last_change = -1

    def derive_key(self, change, index):
        path = './'+str(change)+'/'+str(index)
        hash = self.xpub.derive(path).key.hash()
        if self.address == 'nested':
            return str(P2shAddress.from_script(P2wpkhAddress(hash, version=0).to_script()))

    @staticmethod
    def addr_is_used(addr):
        url = 'https://blockchain.info/q/getreceivedbyaddress/' + addr
        return float(requests.get(url,timeout=10).text) != 0

    def load_data(self):
        self.balance['BTC'] = 0
        for change in [0,1]:
            used = True
            i = 0
            while used:
                pk = self.derive_key(change,index=i)
                i += 1
                url = 'https://blockchain.info/q/addressbalance/' + pk
                b = float(requests.get(url, timeout=10).text) / 100000000
                self.balance['BTC'] += b
                if b == 0:
                    used = self.addr_is_used(pk)
            if change == 0:
                self.last_spend = i-2
            else:
                self.last_change = i-2
        self.btc = self.balance['BTC']
