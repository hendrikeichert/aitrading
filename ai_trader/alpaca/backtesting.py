from lumibot.entities import Data
from lumibot.data_sources import PandasData
from lumibot.data_sources import AlpacaData
from lumibot.backtesting import PandasDataBacktesting
from lumibot.backtesting import YahooDataBacktesting

from alpaca_custom.alpaca_test import get_stocks_data

class AlpacaBacktesting(PandasDataBacktesting):    
    def __init__(self, datetime_start, datetime_end, **kwargs):
        super().__init__(datetime_start, datetime_end)
        # AlpacaData.__init__(self)
        # PandasDataBacktesting.__init__(self, datetime_start, datetime_end)
        # api_secret = kwargs.get("api_secret")
        # self.alpaca = AlpacaData(config={"API_KEY": api_key, "API_SECRET": api_secret})        

class AlpacaBacktestingDataSource(YahooDataBacktesting):
    def __init__(self, datetime_start, datetime_end, **kwargs):
        super().__init__(datetime_start, datetime_end, **kwargs)

    def _pull_source_symbol_bars(self, symbol, length, timestep, timeshift=None, quote=None):
        return get_stocks_data()

if __name__ == "__main__":
    import os
    from datetime import datetime
    from lumibot.entities import Bars

    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    alpaca = AlpacaData(config={"API_KEY": API_KEY, "API_SECRET": API_SECRET})
    backtesting_start_date = datetime(2022, 1, 1)
    backtesting_end_date = datetime(2022, 12, 31)
    data: Bars = alpaca.get_historical_prices(asset="AAPL", length=10, timestep="day")
    print(data.aggregate_bars(frequency="1d").df)