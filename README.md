A crypto-api wallet consists of a set of Account objects. Account objects communicate with various APIs to get the relevant balance and price data for the associated account. An account can be a Bitcoin address or an address of any other cryptocurrency, an exchange account (e.g. Kraken or Bittrex), or a hierarchical deterministic wallet.

In order to load the data from the API, the account objects use Updatables. Updatable is a class whose instances are associated with a source of data (e.g. a function that loads data from the API), and make sure the downloaded data stays up to date (e.g. by redownloading the data frequently).

See Jupyter Notebook for example usage.
