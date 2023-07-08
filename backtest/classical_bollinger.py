from backtesting import Strategy, Backtest
import pandas_ta as ta
import yfinance as yf


def indicator(data):
    bbands = ta.bbands(data.Close.s, std=1)
    return bbands.to_numpy().T[:3]


class ClassicalBollinger(Strategy):

    def init(self):
        self.bbands = self.I(indicator, self.data)

    def next(self):

        lower = self.bbands[0]
        upper = self.bbands[2]

        if self.position:
            if self.data.Close[-1] > upper[-1]:
                self.position.close()
        else:
            if self.data.Close[-1] < lower[-1]:
                self.buy()


if __name__ == '__main__':
    SPY = yf.Ticker('SPY').history(period = '5y')

    bt = Backtest(SPY, ClassicalBollinger,
                  cash=10000, commission=.002,
                  exclusive_orders=True)

    output = bt.run()
    print(output)
