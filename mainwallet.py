from wallet import wallet
from btc_xpub import btc_xpub
from bitmex_account import bitmex_account
from kraken_account import kraken_account
from eos_account import eos_account
from eth_address import eth_address
from bittrex_account import bittrex_account

ledgeracc = btc_xpub(file='keys/xpub', meta={'name':'ledger'})
bitmexacc = bitmex_account(file='keys/bitmex', meta={'name':'bitmex'})
krakenacc = kraken_account(file='keys/kraken', meta={'name':'kraken'})
eosacc = eos_account(accname='shortestpath', meta={'name':'eos'})
eos_oldacc = eos_account(accname='gqytaojvgmge', meta={'name':'eos_old'})
ethacc = eth_address(file='keys/ethpub', meta={'name':'eth'})
bittrexacc = bittrex_account(file='keys/bittrex', meta={'name':'bittrex'})

w = wallet(ledgeracc, bitmexacc, ethacc, krakenacc, eosacc, bittrexacc, eos_oldacc)
print(w.value_btc())
print(w.value_eur())
