## Documentation
This package can be used to monitor the balances of a variety of cryptocurrency accounts. With crypto stored in multiple addresses, on different blockchains and exchange accounts, it can be inconvenient to use different wallet tools, block explorers and exchanges websites to get an overview of your total crypto portfolio. The goal of this package is to facilitate this process by having a general protocol for acquiring data from an API and formatting it for further review. There is a module for each type of account (e.g. BTC address, ETH address, Kraken account) that loads data from their particular API (e.g. blockchain.info, ethplorer.io, api.kraken.com), and this data can be combined to show the total worth of the crypto associates with those accounts.

This package, written in Python 3, provides a number of classes that play different roles in the process described above. The Account class is a template class from which the classes for each type of cryptocurrency account are derived. It provides some general functionality for loading balance data from an API and formatting it.

The classes derived from the Account class are specific for a particular type of account. This can be a cryptocurrency address from any cryptocurrency, or an XPUB key from a hardware wallet, or an exchange/trading account. The derived classes vary in complexity; where a Bitcoin address only has one property (BTC balance), an Ethereum address can have many ERC20 tokens balances associated with it, and a Bitmex account can have unrealized profits that should be added to it's total worth. Derived classes typically also have some functionality to convert balances between different currencies.

The Wallet class aggregates the data retrieved from Account instances and defines some commands to show the total worth of the portfolio in BTC, USD or EUR.

Finally, each of the class mentioned above makes use of the Updatable class. The Updatable class makes sure that data loaded from an API stays up to date without having to redownload the data every time it is needed.

## Example usage
(see Jupyter notebook demo)

## To do
* Bitmex, Bittrex, Kraken accounts: remove unnecessary code
* Add short project description before Documentation section
* Finish Jupyter notebook example, upload notebook to https://nbviewer.jupyter.org/