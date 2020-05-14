import autoDD
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf


ALPHAVANTAGE_API_KEY = 'AT6ABB92QYICBXX5'


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
    
    def getRealTimeDataForSingleStock(self, stock):
        #Get time data
        ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=stock, interval='1min', outputsize='full')
        data = data.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"})
        data = data.iloc[::-1]
        #data.to_csv('datafeed.csv')
        return data
    def technicalIndicators(self,data,top_stock):
        #Get technical indicators (SMA
        ti = TechIndicators(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
        return ti
    
    def plot(self, data, ti, top_stock):
        sma_data, ti_meta_data = ti.get_sma(symbol=top_stock, interval='1min')
        SMAplot = mpf.make_addplot(sma_data[-50:]['SMA'])
        mpf.plot(data[-50:], type='candlestick', volume=True, title='Last 25 Minutes of ' + top_stock, addplot=SMAplot)
    
    def areThereBullishHammerTimes(self, data):
        #abs(a-b) < Threshold
        #lowThreshold = data['Low'] * 2
        #openThreshold = data['Open'] < data['Close']
        hammerTimesSubSet = data[data['Close'] >= data['High'] - (data['High'] * (1 / 100))]
                                 #and lowThreshold['Low'] < openThreshold['Open']]
        hammerTimesSubSet1 = hammerTimesSubSet[hammerTimesSubSet['Open'] < hammerTimesSubSet['Close']]
        final = hammerTimesSubSet1[hammerTimesSubSet1['Low'] * 2 < hammerTimesSubSet1['Open']]
        return final
    
if __name__ == '__main__':
    scraper = Scraper()
    unscreened_stocks = scraper.unscreenedStocks()
    topStock = scraper.topStock(unscreened_stocks)
    realTimeData = scraper.getRealTimeDataForSingleStock(topStock)
    print(realTimeData)
    print(type(realTimeData.iat[0,0]))
    #lowThreshold = realTimeData['Low'] * 2
   # print(lowThreshold)
    print("HammerTimes")
    lowThreshold = realTimeData['Low'] * 2
    openThreshold = realTimeData['Open'] < realTimeData['Close']
    print(type(lowThreshold))
    print(type(openThreshold))
    hammertimes = scraper.areThereBullishHammerTimes(realTimeData)
    print(hammertimes)
  # print(hammertimes.iat[0])
    technicalIndicators = scraper.technicalIndicators(realTimeData,topStock)
    
    #scraper.plot(realTimeData,technicalIndicators,topStock)
    
    