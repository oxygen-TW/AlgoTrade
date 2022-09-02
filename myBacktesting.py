from backtesting import Backtest, Strategy 
from backtesting.lib import crossover 
from backtesting.test import SMA 
from talib import MACD

import pandas as pd 
import sys, os

from MACD import MACD
from DataHandler.commonTools import DataIO

class SmaCross(Strategy):
    def init(self):
        self.fast_line = self.I(SMA, self.data.Close, 13)
        self.slow_line = self.I(SMA, self.data.Close, 48)

    def next(self):
        if crossover(self.fast_line, self.slow_line):
            print(f"{self.data.index[-1]} Buy: Price: {self.data.Close[-1]}, Slow: {self.slow_line[-5:]}, Fast: {self.fast_line[-5:]}")
            self.buy()

        elif crossover(self.slow_line, self.fast_line):
            print(f"{self.data.index[-1]} Sell: Price: {self.data.Close[-1]}, Slow: {self.slow_line[-5:]}, Fast: {self.fast_line[-5:]}")
            self.sell()

class MACDCross(Strategy):
    def init(self):
        macd = MACD(stockData = self.data.df)
        self.MACD_line =  self.I(macd.MACDLine)
        self.Signal_line = self.I(macd.signalLine)
        self.Hist = self.I(macd.histogram)

    def next(self):
        if crossover(self.MACD_line, self.Signal_line):
            print(f"{self.data.index[-1]} Buy: Price: {self.data.Close[-1]}, Slow: {self.Signal_line[-5:]}, Fast: {self.MACD_line[-5:]}")
            self.buy()

        elif crossover(self.Signal_line, self.MACD_line):
            print(f"{self.data.index[-1]} Sell: Price: {self.data.Close[-1]}, Slow: {self.Signal_line[-5:]}, Fast: {self.MACD_line[-5:]}")
            self.sell()


stock_no = ""
dataDir = "stockData"
if(sys.argv[1] != None):
    stock_no = sys.argv[1]

if(sys.argv[2] != None):
    dataDir = sys.argv[2]

df = DataIO.readCSV(os.path.join(dataDir, f"{stock_no}.csv"))
# df = df.interpolate() #CSV檔案中若有缺漏，會使用內插法自動補值，不一定需要的功能

test = Backtest(
    df,
    SmaCross,
    cash=1000000,
    commission=0.004,
    exclusive_orders=True,
    trade_on_close=True,
)

result = test.run() #執行回測程式並存到result中

print(result)
test.plot(filename=os.path.join("results", f"{stock_no}.html")) #將線圖網頁依照指定檔名保存