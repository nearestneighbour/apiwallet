from account import account, updatable
import requests
from btcpy.setup import setup
from btcpy.structs.hd import ExtendedPublicKey
from btcpy.structs.address import P2shAddress, P2wpkhAddress

setup('mainnet')

# TO DO:
# Separate addresses into different balances (name each, e.g. 'change0, spend1')
# Alternatives for address='nested'

class btc_xpub(account):
    def __init__(self, xpub=None, file=None, address='nested', data={}):
        if xpub == None:
            with open(file) as f:
                xpub = f.readlines()[0].strip()
        self.xpub = ExtendedPublicKey.decode(xpub)
        self.address = address
        super().__init__(data)

    def load_balance(self):
        bal = 0
        for change in [False, True]:
            used = True
            i = 0
            while used:
                pk = self.derive_key(change,index=i)
                i += 1
                url = 'https://blockchain.info/q/addressbalance/' + pk
                b = float(requests.get(url, timeout=10).text) / 100000000
                bal += b
                if b == 0:
                    used = address_is_used(pk)
            #if change:
            #    last_change = i-2
            #else:
            #    last_spent = i-2
        return bal#, last_spent, last_change

    def value_self(self):
        return self.u['balance'].getdata()

    def value_base(self, base):
        if base == 'BTC':
            return self.value_self()
        return None

    def derive_key(self, change, index):
        path = './'+str(change)+'/'+str(index)
        hash = self.xpub.derive(path).key.hash()
        if self.address == 'nested':
            return str(P2shAddress.from_script(P2wpkhAddress(hash, version=0).to_script()))
        return None # raise error

def address_is_used(addr):
    url = 'https://blockchain.info/q/getreceivedbyaddress/' + addr
    return float(requests.get(url,timeout=10).text) != 0
