
import os
import yfinance as yf
import plotly
import pandas
import tickerSymbol
from datetime import date
import datetime, time
import schedule
from nsepython import *


no_days = 300

def getCurrentDate():
    DateToday = "{}-{}-{}".format(date.today().year, date.today().month,date.today().day)
    return str(DateToday)


def getPreviousDate(days):
    previousDate = date.today() - datetime.timedelta(days)
    DateLast = ("{}-{}-{}".format(previousDate.year,previousDate.month, previousDate.day))
    return str(DateLast)

# def downloadData(T):
#     start_time = time. time()
#     try:
#         switcher= {
#             'Day':('90d','1d'),
#             'Hour':('30d','60m'),
#             'Minute':('7d','15m')
#         }
#         t , interval = switcher.get(T)
#         for item in tickerSymbol.N200:
#             data = yf.download(tickers=item+".NS", period=t, interval=interval)
#             data.to_csv('Dataset/{}.csv'.format(item))
#         print("--- %s seconds ---" % (time. time() - start_time))
#         return "Data downloaded Successfully in {} seconds".format((time. time() - start_time))
#     except:
#         return ("Not a valid value")

def downloadHourData():
    print("Downloading hourly data")
    for item in tickerSymbol.N200:
        data = yf.download(tickers=item+".NS", period='30d', interval='60m')
        data.to_csv('Dataset/Hour/{}.csv'.format(item))


def downloadDayData():
    print("Downloading Day data")
    for item in tickerSymbol.N200:
        data = yf.download(tickers=item+".NS", period='90d', interval='1d')
        data.to_csv('Dataset/Day/{}.csv'.format(item))


def downloadMinuteData():
    print("Downloading Minute Data")
    for item in tickerSymbol.N200:
        data = yf.download(tickers=item+".NS", period='7d', interval='15m')
        data.to_csv('Dataset/Minute/{}.csv'.format(item))


def getMarketState():
    if nse_marketStatus().get('marketState')[0].get('marketStatus') == 'Open':
        MarketState = True
    else:
        MarketState = False
    return MarketState

def scheduler():
    # downloadMinuteData()
    # downloadDayData()
    # downloadHourData()
    schedule.every(60).minutes.do(downloadDayData)
    schedule.every(45).minutes.do(downloadHourData)
    schedule.every(10).minutes.do(downloadMinuteData)

    while not getMarketState():
        schedule.run_pending()
        time.sleep(1)
        print("........"*5)



scheduler()