# create a test for the DataCache class

from ai_trader.alpaca.api import AlpacaAPI
from ai_trader.alpaca.utils import collect_creds
from alpaca.data.models.bars import Bar
import unittest
from datetime import datetime

class TestAlpacaAPI(unittest.TestCase):

    def test_stocks(self):
        creds = collect_creds()
        api = AlpacaAPI(creds["API_KEY"], creds["API_SECRET"])
        symbol = "AAPL"
        bar_set = api.get_stocks_data([symbol], datetime(2022, 9, 1), datetime(2022, 9, 2))
        assert bar_set is not None
        assert bar_set.data is not None
        assert symbol in bar_set.data
        assert len(bar_set.data[symbol]) > 0
        bar:Bar = bar_set.data[symbol][0]
        # Check if the bar has the required attributes
        assert hasattr(bar, "close")        

    def test_crypto(self):        
        api = AlpacaAPI("", "") # creds are not required for crypto data
        currency = "BTC/USD"
        bar_set = api.get_crypto_data([currency], datetime(2022, 9, 1), datetime(2022, 9, 2))
        assert bar_set is not None
        assert bar_set.data is not None
        assert currency in bar_set.data
        assert len(bar_set.data[currency]) > 0
        bar:Bar = bar_set.data[currency][0]
        # Check if the bar has the required attributes
        assert hasattr(bar, "close")

    def test_get_news_from_api(self):
        creds = collect_creds()
        api = AlpacaAPI(creds["API_KEY"], creds["API_SECRET"])
        api.initialize()
        symbol = "AAPL"
        news = api.get_news_from_api(symbol=symbol, start_date="2022-09-01", end_date="2022-09-02")
        assert news is not None
        assert len(news) > 0
        news_item = news[0]
        # Check if the news item has the required attributes
        assert hasattr(news_item, "headline")
        assert hasattr(news_item, "source")
        assert hasattr(news_item, "summary")
        assert hasattr(news_item, "url")
        assert hasattr(news_item, "created_at")
        assert hasattr(news_item, "updated_at")
        assert hasattr(news_item, "content")
        assert hasattr(news_item, "author")
        assert hasattr(news_item, "images")
        assert hasattr(news_item, "symbols")