import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from DataHandler.commonTools import DataIO

#reference: https://medium.com/codex/how-to-calculate-bollinger-bands-of-a-stock-with-python-f9f7d1184fc3
class BollingerBands():
    def __init__(self, stockData: pd.DataFrame, rate=20):
        self.stockData = stockData

        assert(type(stockData) == pd.DataFrame), "stockData must be a DataFrame"
        assert("Close" in self.stockData.columns), "Close column not found in stockData"

        self.closeingPrice = stockData['Close'] 
        self.rate = rate
        self.bollinger_up, self.bollinger_down = self.calculateBollingerBands()
    
    def calculateSMA(self):
        return self.closeingPrice.rolling(self.rate).mean()

    def calculateBollingerBands(self):
        sma = self.calculateSMA()
        std = self.closeingPrice.rolling(self.rate).std()
        bollinger_up = sma + std * 2 # Calculate top band
        bollinger_down = sma - std * 2 # Calculate bottom band
        return bollinger_up, bollinger_down
    
    def drawPicture(self):
        plt.figure(figsize=(12, 8))
        plt.plot(self.stockData['Close'], label='Close')
        plt.plot(self.bollinger_up, label='Bollinger up')
        plt.plot(self.bollinger_down, label='Bollinger down')
        plt.legend(loc='upper left')
        plt.show()

    def getBollingerBands(self) -> tuple:
        return self.bollinger_up, self.bollinger_down

    def getBollingerBands_Up(self) -> pd.Series:
        return self.bollinger_up
    
    def getBollingerBands_Down(self) -> pd.Series:
        return self.bollinger_down

if(__name__ == "__main__"): 
    symbol = '2330.TW'
    df = DataIO.readCSV(os.path.join("stockData", symbol + ".csv"))
    df.index = np.arange(df.shape[0]) # Convert the index to array from [0, 1, 2, ...number of rows]

    bb = BollingerBands(df)
    print(bb.getBollingerBands_Up())

