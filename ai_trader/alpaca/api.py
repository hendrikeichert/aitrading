import alpaca_trade_api as tradeapi
import json
import datetime
import requests
import sqlite3
import os
from bs4 import BeautifulSoup
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.models.bars import BarSet
from ai_trader.alpaca.cache import DataCache

def default(o):
    if hasattr(o, '__dict__'):
        return o.__dict__
    elif isinstance(o, datetime.datetime):
        return o.isoformat()
    else:
        return str(o)

class AlpacaAPI():

    BASE_URL = 'https://paper-api.alpaca.markets/v2'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def initialize(self):
        self.api = tradeapi.REST(base_url=AlpacaAPI.BASE_URL, key_id=self.api_key, secret_key=self.api_secret)
        self.cache = DataCache()        
        
    def get_news_from_api(self, symbol, start_date, end_date):
        return self.api.get_news(symbol=symbol, start=start_date, end=end_date)
    
    def get_news(self, symbol, start_date, end_date):
        news = self.cache.get_news(symbol, start_date, end_date)
        if news is None:
            news = self.get_news_from_api(symbol, start_date, end_date)
            self.cache.save_news(symbol, start_date, end_date, news)
        return news
    
    def save_to_file(self, filename, news_list):
        news_dicts = [news_item._raw for news_item in news_list]
        with open(filename, "w") as f:
            json_result = json.dumps(news_dicts, default=default, indent=4)
            f.write(json_result)

    def load_from_file(self, filename):
        with open(filename, "r") as f:            
            return json.loads(f.read())

    def get_article_content(url):
        try:
            # Fetch the page content
            response = requests.get(url)
            response.raise_for_status()  # Will raise an exception for bad status codes
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This is a very generic approach; you'll need to inspect each site to find the correct selector
            # Here, we're looking for what might be the main content of an article
            content = soup.find('article') or soup.find('div', class_='article-content') or soup.find('div', id='article-body')
            
            if content:
                return content.get_text(strip=True)
            else:
                return "Content not found or site structure changed."
        
        except requests.RequestException as e:
            return f"Error fetching the URL: {e}"
        

    def get_cached_news(start, end, symbols):
        #         news_cache
    
        # # Check if we've already loaded news for these parameters
        # cache_key = f"{start}_{end}_{'_'.join(symbols)}"
        # if cache_key in news_cache:
        #     return news_cache[cache_key]
        
        # # Check if there's a cached file
        # if os.path.exists(NEWS_CACHE_FILE):
        #     with open(NEWS_CACHE_FILE, 'r') as f:
        #         cached_data = json.load(f)
        #         if cache_key in cached_data:
        #             news_cache[cache_key] = cached_data[cache_key]
        #             return cached_data[cache_key]

        # # If not cached, fetch the news
        # news = self.get_news_from_api(start=start, end=end, symbols=symbols)
        # news_list = [news_item._raw for news_item in news]  # Assuming _raw exists
        # news_cache[cache_key] = news_list
        
        # # Save to file for next time
        # with open(NEWS_CACHE_FILE, 'w') as f:
        #     json.dump(news_cache, f)
        
        # return news_list
        pass

    def get_stocks_data(self, symbols:list, start:datetime, end:datetime)->BarSet:              
        # No keys required for crypto data
        clientStocks = StockHistoricalDataClient(api_key=self.api_key, secret_key=self.api_secret)
        # Creating request object
        request_params = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=TimeFrame.Day,
            start=start,
            end=end
        )

        # Retrieve daily bars for stock symbols in a DataFrame
        return clientStocks.get_stock_bars(request_params)
    
    def get_crypto_data(self, currencies:list, start:datetime, end:datetime)->BarSet:
        """
        Get crypto data
        currencies: list of crypto definition like ["BTC/USD"]
        start: datetime object start date, like datetime(2022, 9, 1)
        end: datetime object end date, like datetime(2022, 9, 7)
        """
        # No keys required for crypto data
        clientCrypto = CryptoHistoricalDataClient()

        # Creating request object
        request_params = CryptoBarsRequest(
            symbol_or_symbols=currencies,
            timeframe=TimeFrame.Day,
            start=start,
            end=end
        )

        # Retrieve daily bars for Bitcoin in a DataFrame and printing it
        return clientCrypto.get_crypto_bars(request_params)         


if __name__ == "__main__":
    from ai_trader.alpaca.utils import collect_creds
    creds = collect_creds()
    alpaca = AlpacaAPI(api_key=creds["API_KEY"], api_secret=creds["API_SECRET"])
    filename = "news.json"
    # news = alpaca.get_news(symbol="AAPL", start_date="2022-03-01", end_date="2022-03-03")
    # alpaca.save_to_file(filename, news)
        
    # news = alpaca.load_from_file(filename)

    # # print(json.dumps(news, default=default, indent=4))
    # for news_item in news:
    #     print(news_item["headline"])
    #     print(news_item["url"])
    #     print(AlpacaAPI.get_article_content(news_item["url"]))
    #     print("\n\n")        