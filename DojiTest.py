import alpaca_trade_api as api
import datetime
import pandas as pd
import self as self
import dbConnector as db

BASE_URL = "https://paper-api.alpaca.markets"
KEY_ID = "PKTAKBFROQY3CPRTEAK4"
SECRET_KEY = "gsBf1RofsWoQRexZobxhxd4sVScmNzDG6zY92x83"


class PythonDojiTrader:
    def get_data(self, symbol, bar, interval, start):
        pacabar = api.get_barset(symbol, interval, limit=1)
        macd_bar = pacabar['MACD']
        candle_size = bar.high - bar.low
        return macd_bar

    def isDoji(symbol, bar, interval, limit):
        if bar[0]['open'] > bar[1]['open'] and bar[2]['open'] < bar[1]['open']:
            if bar[0]['volume'] > bar[1]['volume'] and bar[2]['volume'] > bar[1]['volume'] and bar[4].c > bar[3].c:
                if abs(bar[0].o) - abs(bar[0].c) <= bar[0].c(0.10):
                    if bar[0].h - bar[0].l > bar[0].c:
                        if bar[0].c >= bar[0].o and bar[0].o - bar[0].l > 0.01:
                            return True


    def moving_average(self, symbol, interval, limit, start):

        bar = api.get_barset(symbol, interval, limit)

        minutes = []
        window_period = 0.0
        i = 0
        moving_average = 0.0
        avg_change = 0.0
        stock_price = 0.0

        stock_price = stock_price - (stock_price * 0.05)

        for x in bar:
            i += 1

        moving_average = avg_change / window_period

        if bar[10].c <= bar[5].c and bar[5].c <= bar[1].c:



                return moving_average

    def create_order(self, db, side, symbol, type, qty, time_in_force):

        trade_Time = datetime.datetime() - datetime.timedelta(minutes=1)
        trade_Window = datetime.datetime() - datetime.timedelta(minutes=7)

        bar = self.get(symbol, qty, trade_Time)


        if self.isDoji(bar) and self.shortMovingAverage:
            api.submit_order(
            symbol=symbol,
            side='buy',
            type='market',
            qty=100,
            time_in_force='min',
            order_class='bracket',
            take_profit=dict(
                limit_price=bar[0].c + .5,
            ),
            stop_loss=dict(
                stop_price=bar[0].c - .5,
            )

        )

print('Order Submitted')

if __name__ == '__main__':
    api = api.REST(KEY_ID, SECRET_KEY, BASE_URL)

    account = api.get_account()



