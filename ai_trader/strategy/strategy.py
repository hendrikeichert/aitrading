from timedelta import Timedelta
from MLTradingBot.finbert_utils import estimate_sentiment
from pybroker.context import ExecContext



class MLTrader():

    def __init__(self):
        self.ctx = None
        self.symbol = None
        self.cash_at_risk = .02
        self.last_trade = None
        self.news_handler = None

    def position_sizing(self):               
        cash = float(self.ctx.cash)
        last_price = float(self.ctx.close[0])        
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity

    def get_dates(self): 
        today = self.ctx.dt
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')
    
    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()
        news = self.news_handler.get_news(symbol=self.ctx.symbol, 
                                    start_date=three_days_prior, 
                                    end_date=today) 
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment 

    def on_trading_iteration(self, ctx: ExecContext):
        if self.ctx is None:
            self.ctx = ctx
        cash, last_price, quantity = self.position_sizing() 
        probability, sentiment = self.get_sentiment()

        if cash > last_price: 
            if sentiment == "positive" and probability > .999: 
                if self.last_trade == "sell": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket", 
                    take_profit_price=last_price*1.20, 
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order) 
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999: 
                if self.last_trade == "buy": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price*.8, 
                    stop_loss_price=last_price*1.05
                )
                self.submit_order(order) 
                self.last_trade = "sell"

    def buy_low(self, ctx):
        # If shares were already purchased and are currently being held, then return.
        if ctx.long_pos():
            return
        # If the latest close price is less than the previous day's low price,
        # then place a buy order.
        if ctx.bars >= 2 and ctx.close[-1] < ctx.low[-2]:
            # Buy a number of shares that is equal to 25% the portfolio.
            ctx.buy_shares = ctx.calc_target_shares(0.25)
            # Set the limit price of the order.
            ctx.buy_limit_price = ctx.close[-1] - 0.01
            # Hold the position for 3 bars before liquidating (in this case, 3 days).
            ctx.hold_bars = 3

    def short_high(self, ctx):
        # If shares were already shorted then return.
        if ctx.short_pos():
            return
        # If the latest close price is more than the previous day's high price,
        # then place a sell order.
        if ctx.bars >= 2 and ctx.close[-1] > ctx.high[-2]:
            # Short 100 shares.
            ctx.sell_shares = 100
            # Cover the shares after 2 bars (in this case, 2 days).
            ctx.hold_bars = 2