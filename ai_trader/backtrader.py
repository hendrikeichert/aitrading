import alpaca_backtrader_api
import backtrader as bt
import os

# Ensure environment variables are set
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
if api_key is None or api_secret is None:
    raise ValueError("API_KEY and API_SECRET environment variables must be set")

# Alpaca API credentials
ALPACA_API_KEY = api_key
ALPACA_SECRET_KEY = api_secret
ALPACA_PAPER = True  # Use paper trading

# Initialize Alpaca broker
store = alpaca_backtrader_api.AlpacaStore(
    key_id=ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER
)

# Create a broker instance
broker = store.getbroker()

# Create a data feed
DataFactory = store.getdata
data = DataFactory(dataname='AAPL', historical=True, fromdate=datetime(2021, 1, 1), todate=datetime(2021, 12, 31))

# Define a simple strategy
class TestStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=15)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy(size=10)
        elif self.data.close[0] < self.sma[0]:
            self.sell(size=10)

# Initialize Cerebro engine
cerebro = bt.Cerebro()

# Add data feed to Cerebro
cerebro.adddata(data)

# Add strategy to Cerebro
cerebro.addstrategy(TestStrategy)

# Set broker
cerebro.setbroker(broker)

# Run backtest
cerebro.run()

# Plot the results
cerebro.plot()