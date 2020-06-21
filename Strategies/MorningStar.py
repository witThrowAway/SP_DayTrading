import alpaca_trade_api as api
import datetime
import pandas as pd
import dbConnector as db
import numpy as np

BASE_URL = "https://paper-api.alpaca.markets"
KEY_ID = "PKTAKBFROQY3CPRTEAK4"
SECRET_KEY = "gsBf1RofsWoQRexZobxhxd4sVScmNzDG6zY92x83"

class PythonStarTrader:
    def get_star(self, symbol, bar, interval, limit, start):
        pacabar = api.get_barset(symbol, interval, limit=1)
        simple_moving_average = pacabar['SMA']
        candle_size = bar.high - bar.low
        return simple_moving_average

    def __init__(self):
        print("dbObject created")

    def isMorningStar(self, bar):
    #make original if statement for (5,8,13) that is also how avg will be calculated

        if bar[0]['open'] > bar[1]['open'] and bar[2]['open'] < bar[1]['open']:

            if bar[0]['volume'] > bar[1]['volume'] and bar[2]['volume'] > bar[1]['volume']:

                if bar[0].l >= bar[1].l and bar[2].l < bar[0].l and bar[1].l:

                    return True

    #Idea is to get short term 20 min average of a stock going down and reversing(5,8,13 bar avgs)
    def shortMovingAverage(self, symbol, interval, window, dataSet, start):
        bar = api.get_barset(symbol, interval, limit=5, after=start)
        minutes = []
        window_period = 0.0
        i = 0
        moving_average = 0.0

        weights = np.repeat(1.0, window) /window
        smas = np.convolve(symbol, weights, 'valid')

        for x in dataSet[0:13]:
            i += 1
            moving_average = window_period / minutes

        if bar[10].c <= bar[5].c and bar[5].c <= bar[1].c:
            return moving_average

        print (moving_average)



    def create_order(self, db, side, symbol, type, qty, time_in_force):

        trade_Time = datetime.datetime() - datetime.timedelta(minutes=1)
        trade_Window = datetime.datetime() - datetime.timedelta(minutes=7)

        bar = self.get(symbol, qty, trade_Time)

        #symbol_bars = api.get_barset(symbol, 'minute', 1).df.iloc[0]
        #symbol_price = symbol_bars[symbol]['close']

        if self.isMorningStar(bar) and self.shortMovingAverage:

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

    #connector = db.dbConnector()
    #connection = connector.createConnection()
    #result = connector.getBarsByBarType(connection, 'barType')


    data = [{'id': 189, 'symbol': 'GNUS', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 6158, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 31, 12), 'barType': 'barType'}, {'id': 190, 'symbol': 'GNUS', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 6158, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 31, 58), 'barType': 'barType'}, {'id': 191, 'symbol': 'GNUS', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 11134, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 33, 18), 'barType': 'barType'}, {'id': 192, 'symbol': 'GNUS', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 19456, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 36, 28), 'barType': 'barType'}, {'id': 193, 'symbol': 'GNUS', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 1018, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 37, 57), 'barType': 'barType'}, {'id': 194, 'symbol': 'GNUS', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 2246, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 44, 14), 'barType': 'barType'}, {'id': 195, 'symbol': 'GNUS', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 4800, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 33), 'barType': 'barType'}, {'id': 196, 'symbol': 'DGLY', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 802, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 34), 'barType': 'barType'}, {'id': 197, 'symbol': 'CBD', 'high': 13, 'low': 13, 'open': 13, 'close': 13, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 34), 'barType': 'barType'}, {'id': 198, 'symbol': 'XSPA', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 1378, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 35), 'barType': 'barType'}, {'id': 199, 'symbol': 'MNLO', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 610, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 35), 'barType': 'barType'}, {'id': 200, 'symbol': 'NTEC', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 36), 'barType': 'barType'}, {'id': 201, 'symbol': 'MARK', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 400, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 36), 'barType': 'barType'}, {'id': 202, 'symbol': 'NERV', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 37), 'barType': 'barType'}, {'id': 203, 'symbol': 'NBRV', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 400, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 37), 'barType': 'barType'}, {'id': 204, 'symbol': 'LTM', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 2400, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 37), 'barType': 'barType'}, {'id': 205, 'symbol': 'KTOV', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 1600, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 38), 'barType': 'barType'}, {'id': 206, 'symbol': 'BNGO', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 2800, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 38), 'barType': 'barType'}, {'id': 207, 'symbol': 'AND', 'high': 10, 'low': 10, 'open': 10, 'close': 10, 'volume': 100, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 38), 'barType': 'barType'}, {'id': 208, 'symbol': 'VISL', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 100, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 38), 'barType': 'barType'}, {'id': 209, 'symbol': 'DPW', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 38), 'barType': 'barType'}, {'id': 210, 'symbol': 'INPX', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 400, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 39), 'barType': 'barType'}, {'id': 211, 'symbol': 'MARA', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 6200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 39), 'barType': 'barType'}, {'id': 212, 'symbol': 'SOLO', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 109, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 39), 'barType': 'barType'}, {'id': 213, 'symbol': 'MGI', 'high': 3, 'low': 3, 'open': 3, 'close': 3, 'volume': 1402, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 40), 'barType': 'barType'}, {'id': 214, 'symbol': 'TTOO', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 3000, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 40), 'barType': 'barType'}, {'id': 215, 'symbol': 'IBIO', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 40), 'barType': 'barType'}, {'id': 216, 'symbol': 'TGLS', 'high': 5, 'low': 5, 'open': 5, 'close': 5, 'volume': 100, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 41), 'barType': 'barType'}, {'id': 217, 'symbol': 'SHIP', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 1180, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 41), 'barType': 'barType'}, {'id': 218, 'symbol': 'AMR', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 1300, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 41), 'barType': 'barType'}, {'id': 219, 'symbol': 'UAVS', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 500, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 42), 'barType': 'barType'}, {'id': 220, 'symbol': 'CETX', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 42), 'barType': 'barType'}, {'id': 221, 'symbol': 'POAI', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 400, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 42), 'barType': 'barType'}, {'id': 222, 'symbol': 'ACHV', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 1500, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 42), 'barType': 'barType'}, {'id': 223, 'symbol': 'RIOT', 'high': 3, 'low': 3, 'open': 3, 'close': 3, 'volume': 100, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 42), 'barType': 'barType'}, {'id': 224, 'symbol': 'MVIS', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 43), 'barType': 'barType'}, {'id': 225, 'symbol': 'RNWK', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 44), 'barType': 'barType'}, {'id': 226, 'symbol': 'QLGN', 'high': 6, 'low': 6, 'open': 6, 'close': 6, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 44), 'barType': 'barType'}, {'id': 227, 'symbol': 'PCTI', 'high': 7, 'low': 7, 'open': 7, 'close': 7, 'volume': 100, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 44), 'barType': 'barType'}, {'id': 228, 'symbol': 'CJJD', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 1200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 44), 'barType': 'barType'}, {'id': 229, 'symbol': 'EOD', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 44), 'barType': 'barType'}, {'id': 230, 'symbol': 'TOPS', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 33237, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 45), 'barType': 'barType'}, {'id': 231, 'symbol': 'FRSX', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 3100, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 45), 'barType': 'barType'}, {'id': 232, 'symbol': 'NOVN', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 960, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 46), 'barType': 'barType'}, {'id': 233, 'symbol': 'CPHI', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 47), 'barType': 'barType'}, {'id': 234, 'symbol': 'ONTX', 'high': 0, 'low': 0, 'open': 0, 'close': 0, 'volume': 5200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 49), 'barType': 'barType'}, {'id': 235, 'symbol': 'HTZ', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 52), 'barType': 'barType'}, {'id': 236, 'symbol': 'DKNG', 'high': 40, 'low': 40, 'open': 40, 'close': 40, 'volume': 6476, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 52), 'barType': 'barType'}, {'id': 237, 'symbol': 'EXPR', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 52), 'barType': 'barType'}, {'id': 238, 'symbol': 'BHTG', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 53), 'barType': 'barType'}, {'id': 239, 'symbol': 'TENX', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 845, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 53), 'barType': 'barType'}, {'id': 240, 'symbol': 'MGM', 'high': 18, 'low': 18, 'open': 18, 'close': 18, 'volume': 1110, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 53), 'barType': 'barType'}, {'id': 241, 'symbol': 'TBLT', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 250, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 54), 'barType': 'barType'}, {'id': 242, 'symbol': 'RING', 'high': 28, 'low': 28, 'open': 28, 'close': 28, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 55), 'barType': 'barType'}, {'id': 243, 'symbol': 'INSE', 'high': 4, 'low': 4, 'open': 4, 'close': 4, 'volume': 200, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 55), 'barType': 'barType'}, {'id': 244, 'symbol': 'DCAR', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 100, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 56), 'barType': 'barType'}, {'id': 245, 'symbol': 'OPK', 'high': 2, 'low': 2, 'open': 2, 'close': 2, 'volume': 1804, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 56), 'barType': 'barType'}, {'id': 246, 'symbol': 'MTP', 'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 400, 'shareCount': 1, 'timestamp': datetime.datetime(2020, 6, 2, 14, 45, 57), 'barType': 'barType'}]

    v1 = data[5]['volume']
    print(v1)
    p1 = data[1]['symbol']
    print(p1)

    print(account)
    trader = PythonStarTrader()
    print(trader.isMorningStar(data))

