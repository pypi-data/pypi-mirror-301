import backtrader as bt
from datetime import timezone

__ALL__ = ['MyStrategy']

class MyStrategy(bt.Strategy):

    def __init__(self):
        super(MyStrategy, self).__init__()
        self.dataclose = self.datas[0].close
        self._account_values = []
        self._dates = []
        self._buy_signals = []
        self._sell_signals = []

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self._buy_signals.append((self.datas[0].datetime.datetime(0).replace(tzinfo=timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f"), order.executed.price))
            elif order.issell():
                self._sell_signals.append((self.datas[0].datetime.datetime(0).replace(tzinfo=timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f"), order.executed.price))
    
    def next(self):
        self._account_values.append(self.broker.getvalue())
        self._dates.append(self.datas[0].datetime.datetime(0).replace(tzinfo=timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f"))
    
    def get_account_values(self):
        return self._account_values
    
    def get_dates(self):
        return self._dates

    def get_buy_signals(self):
        return self._buy_signals

    def get_sell_signals(self):
        return self._sell_signals