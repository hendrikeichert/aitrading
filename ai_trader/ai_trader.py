import logging

from ai_trader.alpaca.utils import collect_creds
from ai_trader.alpaca.api import AlpacaAPI

# define the logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

class AiTrader:

    def __init__(self):
        self.alpaca = None

    def initialize(self):        
        logger.info('initialize')
        creds = collect_creds()
        self.alpaca = AlpacaAPI(api_key=creds["API_KEY"], api_secret=creds["API_SECRET"])
        self.alpaca.initialize()


    def stock_example(self):
        logger.info('stock_example')

        stock_data = self.alpaca.get_stocks_data(symbols=['AAPL'], start='2022-03-01', end='2022-03-03')
        print(stock_data)

    def crypto_example(self):
        logger.info('crypto_example')

        crypto_data = self.alpaca.get_crypto_data(currencies=['BTC/USD'], start='2022-03-01', end='2022-03-03')
        print(crypto_data)

    def news_example(self):
        logger.info('news_example')

        news = self.alpaca.get_news_from_api(symbol='AAPL', start_date='2022-03-01', end_date='2022-03-03')
        print(news)

