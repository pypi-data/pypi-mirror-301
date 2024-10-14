import backtrader as bt

class MySharpeRatio(bt.analyzers.SharpeRatio):
    _name = 'mysharpe'

    def __init__(self):
        super(MySharpeRatio, self).__init__()
    
    def stop(self):
        super(MySharpeRatio, self).stop()
        print(f"mysharpe: {self.ratio:.4f}")