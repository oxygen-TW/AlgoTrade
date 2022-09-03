import yfinance as yf
import os

from commonTools import DataIO

def getData(stockNo, start, end):
    stockData = yf.download(stockNo, start=start, end=end)
    stockData = stockData.drop(["Adj Close"], axis=1)
    stockData.to_csv(os.path.join("stockData", stockNo + '.csv'))
    return stockData


if(__name__ == "__main__"):
    startDate = '2022-01-01'
    endDate = '2022-08-29'
    stockNo = '2383.TW'

    getData(stockNo, startDate, endDate)

    # ## 直接呼叫回測腳本
    # ##TODO: Dont use fixed path
    os.system(f"python myBacktesting.py {stockNo} stockData")