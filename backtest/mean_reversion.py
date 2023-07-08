from backtesting import Strategy, Backtest
from backtesting.test import SMA
import yfinance as yf

class MeanReversion(Strategy):
    w = 15
    d = 0.02

    def init(self):
        close = self.data.Close
        self.sma = self.I(SMA, close, self.w)

    def next(self):
        if self.position:
            if self.data.Close[-1] > (1 + self.d) * self.sma[-1]:
                self.position.close()
        else:
            if self.data.Close[-1] < (1 - self.d) * self.sma[-1]:
                self.buy()


if __name__ == '__main__':
    SPY = yf.Ticker('SPY').history(period='5y')
    bt = Backtest(SPY, MeanReversion,
                  cash=10000, commission=0.0,
                  exclusive_orders=True)

    output = bt.run()
    #stats = bt.optimize(w=range(5, 90, 5), maximize='Sharpe Ratio')

    print(output)
    bt.plot()
