import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta


BASE_URL = "https://paper-api.alpaca.markets"
KEY_ID = "PKTAKBFROQY3CPRTEAK4"
SECRET_KEY = "gsBf1RofsWoQRexZobxhxd4sVScmNzDG6zY92x83"


def main():
    print("Starting Doji Reversal Retriever...")

def gather_data(symbol, interval, limit, start, end, window_range):



def simple_moving_avg(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas

print(simple_moving_avg(dataset))

#Predicting bullish reversal trend
def isDojiBar(symbol, interval, limit):
    stock_price = api.get_barset(symbol, interval, limit)
    stop_price =  stock_price - (stock_price * 0.005)
    if bar.close >= bar.open and bar.open - bar.low > 0.05:
#confirmation
    if stock_price = stock_price - (stock_price * 0.005)

     return True
     print("Buying on Doji Candlestick Pattern!")
   def  self.alpaca.submit_order("MSFT", 1, 'buy', 'market', 'day')



    def prices(symbols):
        now = pd.Timestamp.now(tz=easterntz)

        return _get_prices(symbols, now)

'''Get the map of DataFrame price data from Alpaca's data API.'''

start_dt = now - pd.timedelta('50 days')

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type.,
        "time_in_force": time_in_force
    }

r = requests.post(Oders)

def get_barset(symbols):
    return api.get_barset(
        symbols,
        'day',
        limit = 7,
        start=start_dt,
        end=now
    )

class PythonTradingBot :
    def: __init__(self):
    self.alpaca = tradeapi.REST('PKTAKBFROQY3CPRTEAK4', 'gsBf1RofsWoQRexZobxhxd4sVScmNzDG6zY92x83', alpaca_BASE_URL, api_version='v2'

     def run(self)  :
        #On Each Minute

        async def on_minute(cann, channel, bar):

        # Entry
        if bar.close >= bar.open and bar.open - bar.low > 0.1:
            print("Buying on Doji Candlestick Pattern!")
            self.alpaca.submit_order("MSFT", 1, 'buy', 'market', 'day')



        conn.run(['AM.MSFT'])

