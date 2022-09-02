from http.client import TOO_MANY_REQUESTS
import json
import yfinance as yf
import os
import datetime
from pandas import concat, DataFrame, DatetimeIndex
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

def getFTXData(crypto, start, end, save=True, resolution=60) -> DataFrame:
    #Convert start and end to unix time
    startDate = datetime.datetime.strptime(start, "%Y-%m-%d")
    #endDate -= 1 day for for loop indexing
    endDate = datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.timedelta(days=1)
    
    #Get data from api: GET https://ftx.com/api/indexes/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time} from startDate to endDate with step=1 day
    data = DataFrame()
    assert(len(data) == 0), "New dataframe should be empty"

    #For loop start at start and end at end with step of 1 day
    
    indexDay = startDate
    while(indexDay < endDate):
        #show date progress in HH:MM:SS
        logging.info(f"Fetching data for {indexDay.strftime('%Y-%m-%d')}")

        nextDay = (indexDay + datetime.timedelta(days=1)).timestamp()
        
        #Convert indexDay to unix time
        indexDay = indexDay.timestamp()
        

        url = f"https://ftx.com/api/indexes/{crypto}/candles?resolution={resolution}&start_time={indexDay}&end_time={nextDay}"
        
        r = requests.get(url)
        
        if(r.status_code != 200):
            print(f"Error: {r.status_code}")
            exit(1)
            
        if(r.json()["success"] == False):
            print(f"Error: {r.json()['error']}")
            exit(1)

        logging.debug(DataFrame(r.json()["result"]))
        res = json.loads(r.text)

        logging.debug(res["result"][0])
        #concat new data to data
        data = concat([data, DataFrame(res["result"])])

        logging.debug("Data Inner->" + str(data.shape))
        logging.debug("Res Inner->" + str(DataFrame(res["result"]).shape))

        indexDay = datetime.datetime.fromtimestamp(indexDay) + datetime.timedelta(days=1)

    logging.info(data.head())
    logging.debug(data.shape)

    if(save):
        data.to_csv(os.path.join("cryptoData", crypto + '_ftx.csv'))

    return data

    # return crypto_data
if(__name__ == "__main__"):
    startDate = '2022-08-01'
    endDate = '2022-08-29'
    crypto = 'BTC'

    # getData(crypto, startDate, endDate)
    getFTXData(crypto, "2022-08-28", "2022-09-05")

    # ## 直接呼叫回測腳本
    # ##TODO: Dont use fixed path
    #os.system(f"python myBacktesting.py {crypto}_1m cryptoData")