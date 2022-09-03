import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf

from DataHandler.commonTools import DataIO


class StochasticOscillator():
    def __init__(self, data, period=14, Kt=3, RSIt=3):
        self.stockData = data
        self.period = period
        self.Kt = Kt
        self.RSIt = RSIt

    def calculateRSI(self):
        highestHigh = self.stockData['High'].rolling(self.period).max()
        lowestLow = self.stockData['Low'].rolling(self.period).min()
        return (self.stockData['Close'] - lowestLow) / (highestHigh - lowestLow)

    def calculateK(self):
        return self.calculateRSI().rolling(self.Kt).mean()

    def calculateD(self):
        return self.calculateK().rolling(self.RSIt).mean()

    def drawPicture(self):
        candleData = self.stockData[['Open', 'High', 'Low', 'Close', 'Volume']]
        stoch = [
            mpf.make_addplot(self.calculateK(), panel=1, secondary_y=True, color='blue', title="Blue: K line, Orange: D line"),
            mpf.make_addplot(self.calculateD(), panel=1, secondary_y=False, color='orange')
        ]

        mpf.plot(candleData, type='candle', style='binance',
                 addplot=stoch, figratio=(18, 10), title='Stochastic Oscillator')


if (__name__ == "__main__"):
    symbol = '2330.TW'
    df = DataIO.readCSV(os.path.join("stockData", symbol + ".csv"))
    # df.index = np.arange(df.shape[0]) # Convert the index to array from [0, 1, 2, ...number of rows]

    print(df.head())
    sotch = StochasticOscillator(df)
    print(sotch.calculateK())
    sotch.drawPicture()
