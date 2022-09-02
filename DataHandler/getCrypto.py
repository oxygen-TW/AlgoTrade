import yfinance as yf
import os

def getData(crypto, start, end):
    crypto_data = yf.download(crypto, start=start, end=end)
    crypto_data = crypto_data.drop(["Adj Close"], axis=1)
    crypto_data.to_csv(os.path.join("cryptoData", crypto + '.csv'))
    return crypto_data


if(__name__ == "__main__"):
    startDate = '2022-01-01'
    endDate = '2022-08-29'
    crypto = 'BTC-USD'

    getData(crypto, startDate, endDate)

    # ## 直接呼叫回測腳本
    # ##TODO: Dont use fixed path
    os.system(f"python myBacktesting.py {crypto} cryptoData")