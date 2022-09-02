import pandas as pd
import sys, os
import yfinance as yf
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

from DataHandler.commonTools import DataIO

class MACD():
    def __init__(self, stockData:DataFrame, _DIFF:int = 12, _DEA:int = 26, _MACD:int = 9):
        self.stockData = stockData
        self.stockData['200EMA'] = self.stockData['Close'].ewm(span = 200).mean()
        self.stockData['fastEMA'] = self.stockData['Close'].ewm(span = _DIFF).mean()
        self.stockData['slowEMA'] = self.stockData['Close'].ewm(span = _DEA).mean()
        self.stockData['MACD'] = self.stockData['fastEMA'] - self.stockData['slowEMA']
        self.stockData['signal'] = self.stockData['MACD'].ewm(span = _MACD).mean()
        self.stockData['hist'] = self.stockData['MACD'] - self.stockData['signal']
        self.stockData['green_hist'] = np.where(self.stockData['hist'] > 0, self.stockData['hist'], 0)
        self.stockData['red_hist'] = np.where(self.stockData['hist'] < 0, self.stockData['hist'], 0)
        #self.candle_data = self.stockData[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    def drawPicture(self):
        candleData = self.stockData[['Open', 'High', 'Low', 'Close', 'Volume']]
        macd = [mpf.make_addplot(self.stockData['200EMA'], panel = 0, secondary_y = False, color = 'red'),
                mpf.make_addplot(self.stockData['MACD'], panel = 1, secondary_y = True, color = 'blue'),
                mpf.make_addplot(self.stockData['signal'], panel = 1, secondary_y = False, color = 'orange'),
                mpf.make_addplot(self.stockData['green_hist'], panel = 1, secondary_y = False, type = 'bar', color = 'green'),
                mpf.make_addplot(self.stockData['red_hist'], panel = 1, secondary_y = False, type = 'bar', color = 'red')
        ]

        mpf.plot(candleData, type = 'candle', style = 'binance', addplot = macd, figratio = (18, 10), title = 'MACD')

    def signalLine(self) -> Series:
        return self.stockData['signal']
    
    def MACDLine(self) -> Series:
        return self.stockData['MACD']

    def histogram(self) -> Series:
        return self.stockData['hist']
    
    # def signalLineNp(self) -> np.ndarray:
    #     return np.array(self.stockData['signal'])
    
    # def MACDLineNp(self) -> np.ndarray:
    #     return np.array(self.stockData['MACD'])

    # def histogramNp(self) -> np.ndarray:
    #     return np.array(self.stockData['hist'])

if(__name__ == "__main__"):
    data = DataIO().readCSV("stockData\\2610.TW.csv")
    macd = MACD(data)
    print(list(macd.signalLine()))
    macd.drawPicture()