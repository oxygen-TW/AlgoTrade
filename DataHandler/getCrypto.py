import yfinance as yf
import os
import datetime
from pandas import concat, DataFrame
import requests

import logging
logging.basicConfig(level=logging.INFO)

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

    logging.info(data.head())

    if(save):
        data.to_csv(os.path.join("cryptoData", crypto + '_1m.csv'))
    return data

def getFTXData(crypto, start, end, save=True, resolution=60):
    #Convert start and end to unix time
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")

    #generate an list of dates between start and end, with a step of 7 day
    date_list = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days, 7)]
    
    #Convert all dates in date_list to unix time
    date_list = [int(date.timestamp()) for date in date_list]

    #convert start to unix time and append to date_list
    # date_list.append(int(start.timestamp()))
    date_list.reverse()
    
    logging.debug(date_list, start)

    #Get data from api: GET https://ftx.com/api/indexes/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time} for each date in date_list
    data = DataFrame()
    logging.info("Processing data...")

    for i in range(1, len(date_list)):
        print(f"Processing {date_list[i]} to {date_list[i-1]}")
        url = f"https://ftx.com/api/indexes/{crypto}/candles?resolution={resolution}&start_time={date_list[i]}&end_time={date_list[i-1]}"
        
        r = requests.get(url)
        
        if(r.status_code != 200):
            print(f"Error: {r.status_code}")
            exit(1)
            
        if(r.json()["success"] == False):
            print(f"Error: {r.json()['error']}")
            exit(1)

        data = concat([data, DataFrame(r.json()["result"])])
    
    logging.info(data.head())

    if(save):
        data.to_csv(os.path.join("cryptoData", crypto + '_ftx.csv'))

    return data

    # return crypto_data
if(__name__ == "__main__"):
    startDate = '2022-08-01'
    endDate = '2022-08-29'
    crypto = 'BTC'

    # getData(crypto, startDate, endDate)
    getFTXData(crypto, "2021-01-01", "2022-09-05")

    # ## 直接呼叫回測腳本
    # ##TODO: Dont use fixed path
    #os.system(f"python myBacktesting.py {crypto}_1m cryptoData")