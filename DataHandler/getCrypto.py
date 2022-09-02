import yfinance as yf
import os
import datetime
from pandas import concat, DataFrame

def getData(crypto, start, end, save=True, interval="1d"):
    crypto_data = yf.download(crypto, start=start, end=end, interval=interval)
    crypto_data = crypto_data.drop(["Adj Close"], axis=1)
    if(save):
        crypto_data.to_csv(os.path.join("cryptoData", crypto + '.csv'))

    return crypto_data

#Can not fetch >30 days of data
def getMinutsData(crypto, start, end=None, save=True) -> DataFrame:
    base = datetime.datetime.today()
    if(end != None):
        base = datetime.datetime.strptime(end, "%Y-%m-%d")
    start = datetime.datetime.strptime(start, "%Y-%m-%d")

    #calculate days between start and end
    numdays = base - start
    numdays = numdays.days
    
    assert((datetime.datetime.today()-start).days <= 30), "Can not fetch >30 days of data"
    
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays, 1)]

    data = DataFrame()
    for i in range(1, len(date_list)):
        data = concat([data, getData(crypto, date_list[i].strftime("%Y-%m-%d"),  date_list[i-1].strftime("%Y-%m-%d"), save=False, interval="1m")])
    
    data = data.iloc[::-1]

    if(save):
        data.to_csv(os.path.join("cryptoData", crypto + '_1m.csv'))
    return data

if(__name__ == "__main__"):
    startDate = '2022-08-01'
    endDate = '2022-08-29'
    crypto = 'BTC-USD'

    # getData(crypto, startDate, endDate)
    getMinutsData(crypto, "2022-08-04", end="2022-08-29")

    # ## 直接呼叫回測腳本
    # ##TODO: Dont use fixed path
    #os.system(f"python myBacktesting.py {crypto} cryptoData")