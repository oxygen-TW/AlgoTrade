import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf

from DataHandler.commonTools import DataIO


class MovingAverage():
    def __init__(self, data, days) -> None:
        assert(type(data) == pd.DataFrame), "stockData must be a DataFrame"
        assert("Close" in data.columns), "Close column not found in stockData"

        self.stockData = data
        self.days = days

    def SMA(self):
        return self.stockData["Close"].rolling(self.days).mean()

    def drawPicture(self):
        candleData = self.stockData[['Open', 'High', 'Low', 'Close', 'Volume']]
        ma = [
            mpf.make_addplot(self.SMA(), panel=0, secondary_y=True, color='blue', title="SMA")
        ]

        mpf.plot(candleData, type='candle', style='binance',
                 addplot=ma, figratio=(18, 10), title='MovingAverage')

if(__name__ == "__main__"):
    data = DataIO().readCSV("stockData\\2610.TW.csv")
    ma = MovingAverage(data, 7)
    #print(list(macd.signalLine()))
    print(ma.SMA())
    ma.drawPicture()