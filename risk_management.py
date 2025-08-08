import time

class RiskManager:
    def __init__(self, capital, max_alloc_fraction=0.2, stop_loss_pct=0.05, take_profit_pct=0.1, cooldown=3600):
        self.capital = capital
        self.max_alloc_fraction = max_alloc_fraction
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.cooldown = cooldown
        self.last_trade_time = {}

    def can_trade(self, ticker):
        last_time = self.last_trade_time.get(ticker, 0)
        return (time.time() - last_time) > self.cooldown

    def update_trade_time(self, ticker):
        self.last_trade_time[ticker] = time.time()

    def get_max_allocation(self):
        return self.capital * self.max_alloc_fraction

    def check_stop_loss(self, entry_price, current_price):
        return (entry_price - current_price) / entry_price >= self.stop_loss_pct

    def check_take_profit(self, entry_price, current_price):
        return (current_price - entry_price) / entry_price >= self.take_profit_pct
