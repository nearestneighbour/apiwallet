import requests
from btcpy.setup import setup
from btcpy.structs.hd import ExtendedPublicKey
from btcpy.structs.address import P2shAddress, P2wpkhAddress

from .. import Account

setup('mainnet')

# TO DO:
# Separate addresses into different balances (name each, e.g. 'change0, spend1')
# Alternatives for address='nested'

class btc_xpub(Account):
    def __init__(self, xpub=None, file=None, meta={}):
        if xpub == None:
            with open(file) as f:
                xpub = f.readlines()[0].strip()
        self.xpub = ExtendedPublicKey.decode(xpub)
        super().__init__(meta)
        self.native = 'BTC'

    def load_balance(self):
        bal = 0
        for change in [0, 1]:
            used = True
            i = 0
            while used:
                pk = derive_key(self.xpub, change, index=i)
                i += 1
                url = 'https://blockchain.info/q/addressbalance/' + pk
                b = float(requests.get(url, timeout=10).text) / 100000000
                bal += b
                if b == 0:
                    used = address_is_used(pk)
        return {'BTC':bal}

def derive_key(xpub, change, index, address='nested'):
    path = './'+str(change)+'/'+str(index)
    hash = xpub.derive(path).key.hash()
    if address == 'nested':
        return str(P2shAddress.from_script(P2wpkhAddress(hash, version=0).to_script()))
    return None # raise error

def address_is_used(addr):
    url = 'https://blockchain.info/q/getreceivedbyaddress/' + addr
    return float(requests.get(url,timeout=10).text) != 0
