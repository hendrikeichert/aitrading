import pybroker
from datetime import datetime
from pybroker import Strategy, StrategyConfig
from pybroker.data import Alpaca
from ai_trader.alpaca.utils import collect_creds
from strategy import MLTrader
from ai_trader.alpaca.api import AlpacaAPI

# Initialize Alpaca data provider
creds = collect_creds()
alpaca = Alpaca(api_key=creds["API_KEY"], api_secret=creds["API_SECRET"])
pybroker.enable_data_source_cache('aapl')
config = StrategyConfig(initial_cash=100_000)
start_date = datetime.strptime('2022-03-01', '%Y-%m-%d')
end_date = datetime.strptime('2022-04-30', '%Y-%m-%d')
strategy = Strategy(alpaca, start_date, end_date, config=config)
trader = MLTrader()
trader.news_handler = AlpacaAPI(api_key=creds["API_KEY"], api_secret=creds["API_SECRET"])

symbols = ['AAPL']
# trader.on_trading_iteration,
# strategy.add_execution(trader.buy_low, symbols)
strategy.add_execution(trader.short_high, symbols)
result = strategy.backtest(timeframe="1d")

import matplotlib.pyplot as plt
# Plot the market value of the portfolio
# fit the chart according to the size of the window and the given data max values

plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
chart = plt.subplot2grid((1, 1), (0, 0))
chart.plot(result.portfolio.index, result.portfolio['market_value'])
plt.xlabel('Date')
plt.ylabel('Market Value')
plt.title('Portfolio Market Value Over Time')
plt.tight_layout()  # Adjust subplot parameters to give specified padding
# save the chart to a file
# plt.savefig('market_value_low.png')
plt.savefig('market_value_short.png')