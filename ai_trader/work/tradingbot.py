from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime

import os
import time

# set timezone
os.environ['TZ'] = 'Europe/Zurich'  # or your appropriate timezone
time.tzset()

# get value for API_KEY and API_SECRET from env variable with same name
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
os.environ
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CONFIG = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True,
}

# ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
from alpaca_custom.alpaca_test import get_stocks_data

class MLTrader(Strategy):

    parameters = {
        "symbol": "SPY",
        "quantity": 1,
        "side": "buy"
    }

    def initialize(self, symbol:str=""):
        self.symbol = symbol
        self.sleeptime = "1D" #24H
        self.last_trade = None
        self.backtest = True
        self.historical_data = get_stocks_data()
    
    def on_trading_iteration(self):        
        current_date = self.get_datetime().date()
        if current_date in self.historical_data.index:
            price = self.historical_data.loc[current_date].close
            if self.first_iteration:
                qty = self.portfolio_value // price
                order = self.create_order(self.symbol, qty, "buy")
                self.submit_order(order)

if __name__ == "__main__":
    backtesting_start = datetime(2022, 1, 1)
    backtesting_end = datetime(2022, 12, 31)
    
    trader = Trader()
    broker = Alpaca(ALPACA_CONFIG)         
    # broker.IS_BACKTESTING_BROKER = True
    # broker.data_source.datetime_start = datetime_start
    # broker.data_source.datetime_end = datetime_end

    symbol = "SPY"
    strategy = MLTrader(name="mlstrat",
                        budget=10000, 
                        broker=broker,
                        symbol=symbol)
                        #parameters={"sumbol":symbol})    

    from alpaca_custom.backtesting import AlpacaBacktestingDataSource

    strategy.run_backtest(
        AlpacaBacktestingDataSource,
        backtesting_start,
        backtesting_end,
        parameters={"symbol": "SPY"}
    )

    # trader.run_all()

