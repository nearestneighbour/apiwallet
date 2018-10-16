from wallet import wallet
from btc_xpub import btc_xpub
from bitmex_account import bitmex_account
from kraken_account import kraken_account
from eos_account import eos_account
from eth_address import eth_address
from bittrex_account import bittrex_account

ledgeracc = btc_xpub(file='keys/xpub', data={'name':'ledger'})
bitmexacc = bitmex_account(file='keys/bitmex', data={'name':'bitmex'})
krakenacc = kraken_account(file='keys/kraken', data={'name':'kraken'})
eosacc = eos_account(accname='shortestpath', data={'name':'eos'})
eos_oldacc = eos_account(accname='gqytaojvgmge', data={'name':'eos_old'})
ethacc = eth_address(file='keys/ethpub', data={'name':'eth'})
bittrexacc = bittrex_account(file='keys/bittrex', data={'name':'bittrex'})

w = wallet(ledgeracc, bitmexacc, ethacc, krakenacc, eosacc, bittrexacc, eos_oldacc)
w.show('total,balance,currency')
w.save('mywallet')
