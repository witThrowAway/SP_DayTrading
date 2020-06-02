import autoDD
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import alpaca_trade_api as tradeapi
import datetime



#ALPHAVANTAGE_API_KEY = ['4V135H1E1WD8KL2H''1QHMI47XYRQ7TWAO','9FMDAA394M57MTO4','TUN4UO2WBJB6EOP8','I0QTTDE58ZSTDYBV','1TV5Q263WGF2U2WA']
ALPHAVANTAGE_API_KEY = '4V135H1E1WD8KL2H'

class Scraper():

    def unscreenedStocks(self):
        #grab data from autoDD
        unscreened_stocks = autoDD.main()
        print ((unscreened_stocks))
        print(str(len(unscreened_stocks)) + ' stocks found while scraping.')
        return unscreened_stocks
    
    def topStock(self, unscreened_stocks):
        top_stock = unscreened_stocks[0][0]
        return top_stock
    
    def getIntraDayDataForSingleStock(self, stock):
        #Get time data
        ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=stock, interval='1min', outputsize='full')
        data = data.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"})
        data = data.iloc[::-1]
        data.to_csv('datafeed.csv')
        return data
    def getBar(self, symbol, interval,start):
        barset = api.get_barset(symbol, interval, limit=1, after=start)
        return barset
    def getRealTimeDataForSingleStock(self, stock):
        ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=stock, interval = '1min', outputsize= 'full')
        data = data.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"})
        data = data.iloc[::-1]
        return data

    def technicalIndicators(self,data,top_stock):
        #Get technical indicators (SMA
        ti = TechIndicators(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
        return ti
    
    def plot(self, data, ti, top_stock):
        sma_data, ti_meta_data = ti.get_sma(symbol=top_stock, interval='1min')
        SMAplot = mpf.make_addplot(sma_data[-50:]['SMA'])
        mpf.plot(data[-50:], type='candlestick', volume=True, title='Last 25 Minutes of ' + top_stock, addplot=SMAplot)
    
    def areThereBearishHammerTimesInDataFrame(self, data):
        hammerTimesSubSet = data[data['Open'] <= data['High'] - (data['High'] * (1 / 200))]
        hammerTimesSubSet1 = hammerTimesSubSet[hammerTimesSubSet['Open'] > hammerTimesSubSet['Close']]
        final = hammerTimesSubSet1[hammerTimesSubSet1['Low'] * 1.025 < hammerTimesSubSet1['Close']]
        return final
    def simpleMovingAverage(self, startingIndex, endIndex, data):
        simpleMovingAverage = 0.0
        sum = 0.0
        divisor = endIndex - startingIndex
        y = startingIndex
        for x in data:
            y += 1
            sum += data.iat[y, 1]
            if y == endIndex:
                break
        simpleMovingAverage = sum / divisor
        if (data.iat[startingIndex,1] > data.iat[endIndex,1]):
            simpleMovingAverage = -simpleMovingAverage

        return simpleMovingAverage
    
if __name__ == '__main__':
    api = tradeapi.REST()
    scraper = Scraper()
    unscreened_stocks = scraper.unscreenedStocks()
    topStock = scraper.topStock(unscreened_stocks)
    selectedTime = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1)

    #for x in unscreened_stocks:
        #print(x)
    barset = api.get_barset(topStock, '1Min', limit=1, after=selectedTime)
    print(barset)
        #hammertimes = scraper.areThereBullishHammerTimes(realTimeData)
        #print(hammertimes)

    #df = pd.read_csv("/Users/ryangould/Downloads/SP_DayTrading/datafeed.csv")
    #df = scraper.getRealTimeDataForSingleStock(topStock)
   # hammertimes = scraper.areThereBearishHammerTimesInDataFrame(df)
   # simpleMovingAverage = scraper.simpleMovingAverage(379, 382, df)
    #print(hammertimes)
    #print(simpleMovingAverage)
    #print(df)
    #print("??")
    #print(df.iat[1543,0])
   # technicalIndicators = scraper.technicalIndicators(df,topStock)
    
    #scraper.plot(realTimeData,technicalIndicators,topStock)
    
    