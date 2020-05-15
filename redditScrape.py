import autoDD
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf



ALPHAVANTAGE_API_KEY = ['4V135H1E1WD8KL2H''1QHMI47XYRQ7TWAO','9FMDAA394M57MTO4','TUN4UO2WBJB6EOP8','I0QTTDE58ZSTDYBV','1TV5Q263WGF2U2WA']


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
    
    def areThereBearishHammerTimes(self, data):
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
    scraper = Scraper()
    #unscreened_stocks = scraper.unscreenedStocks()
   # topStock = scraper.topStock(unscreened_stocks)
    '''  for x in unscreened_stocks:
        #print(x)
        realTimeData = scraper.getRealTimeDataForSingleStock(x[0])
        hammertimes = scraper.areThereBullishHammerTimes(realTimeData)
        print(hammertimes)
    '''
    df = pd.read_csv("/Users/ryangould/Downloads/SP_DayTrading/datafeed.csv")
    hammertimes = scraper.areThereBearishHammerTimes(df)
    simpleMovingAverage = scraper.simpleMovingAverage(379, 382, df)
    print(hammertimes)
    print(simpleMovingAverage)
    print(df.iat[0,0])
    print(df.iat[379,1])
    print(df.iat[380,1])
    print(df.iat[381,1])
    print(df.iat[382,1])
   # technicalIndicators = scraper.technicalIndicators(df,topStock)
    
    #scraper.plot(realTimeData,technicalIndicators,topStock)
    
    