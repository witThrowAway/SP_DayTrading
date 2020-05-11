import autoDD
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import mplfinance as mpf

ALPHAVANTAGE_API_KEY = 'AT6ABB92QYICBXX5'


if __name__ == '__main__':


    unscreened_stocks = autoDD.main()
    print ((unscreened_stocks))
    print(str(len(unscreened_stocks)) + ' stocks found while scraping.')
    top_stock = unscreened_stocks[0][0]

    #Get time data
    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=top_stock, interval='1min', outputsize='full')
    data = data.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"})
    data = data.iloc[::-1]
    print(data)

    #Get technical indicators (SMA
    ti = TechIndicators(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
    sma_data, ti_meta_data = ti.get_sma(symbol=top_stock, interval='1min')
    rsi_data, rsi_metadata = ti.get_rsi(symbol=top_stock, interval='1min')

    SMAplot = mpf.make_addplot(sma_data[-50:]['SMA'])
    mpf.plot(data[-50:], type='candlestick', volume=True, title='Last 25 Minutes of ' + top_stock, addplot=SMAplot)
