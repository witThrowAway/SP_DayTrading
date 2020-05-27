#!/usr/bin/python
import alpaca_trade_api as api
import datetime
import pandas as pd
import pymysql.cursors
import pymysql
import dbConnector as db

BASE_URL = 'https://paper-api.alpaca.markets'
KEY_ID = 'PKXJ9PFWUR1PV0W4CR3Z'
SECRET_KEY = 'fQPmWsENWU7hrWlxoyGrPDsOOxehqkielyVs3bJ8'

class Strategy:
    def getBar(self, symbol, interval,start):
        barset = api.get_barset(symbol, interval, limit=1, after=start)
        mvis_bars = barset['MVIS']
        return mvis_bars
    def isHammerBar(self, bar):
        if bar[0].o <= (bar[0].h - bar[0].h * (1/200)):
            if bar[0].o > bar[0].c:
                if bar[0].l * 1.025 < bar[0].c:
                    return True
    def simpleMovingAverageAcrossTime(self, symbol, interval,start):
        bar = api.get_barset(symbol, interval, limit=5, after=start)
        sum = 0.0
        simpleMovingAverage = 0.0
        y = 0
        n = 0
        for x in bar:
            y += 1
            n += 1.0
            sum += bar[y].c
        simpleMovingAverage = sum/n
        if bar[0].c > bar[3].c  and bar[3].c > bar[5].c:
            simpleMovingAverage = -simpleMovingAverage

        return simpleMovingAverage

    #function containing a complete strategy
    def hammerTimeTrading(self, df,symbol):
        #selectedTime is always a minute behind the present
        selectedTime = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1)
        #selectedWindow is always X minutes before present
        selectedWindow = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=5)
        #get last minute info for selected symbol
        bar = self.getBar(symbol,'1Min',selectedTime)

        #####block to verify if cronjob runs######
        f = open("/Users/ryangould/Downloads/SP_DayTrading/test.txt", "a")
        f.write(bar)
        f.close()
        #This block can be swapped to database write calls later on
        ##########################################

        #parse out data to add to dataframe
        data = {'Time':[bar[0].t], 'Open':[bar[0].o], 'High':[bar[0].h], 'Low':[bar[0].l], 'Close':[bar[0].c], 'Volume':[bar[0].v]}
        df = df.append(data, ignore_index=True)
        #unused df - need to write to external storage so simpleMovingAverage can read from it
        #to reduce overall API calls

        #check if the current bar is a hammer and the last 5 bars were a negative moving average
        if self.isHammerBar(bar) and self.simpleMovingAverageAcrossTime(symbol,'1Min',selectedWindow) < 0:
            #buy position at hammer (current bar)
            api.submit_order(
                symbol=symbol,
                side='buy',
                type='market',
                qty='100',
                time_in_force='day',
                order_class='bracket',
                take_profit=dict(
                    limit_price=bar[0].c + .5,
                ),
                stop_loss=dict(
                    stop_price=bar[0].c - .5,
                )
            )
            print('ORDER SUBMITTED')

if __name__ == '__main__':

    api = api.REST(KEY_ID, SECRET_KEY, BASE_URL)

    account = api.get_account()


    # Connect to the database
    #connector = db.dbConnector()
    #connection = connector.createConnection()
    #connector.insertBar('symbol', 7, 6, 6, 6, 6, 6, 'barType', connection)
    #print(connector.getBarsBySymbol(connection,'symbol'))
    #print(account.cash)

    #bar = getBar('MVIS','1Min',selectedTime)
    #df = pd.DataFrame(columns=['Time','Open','High','Low','Close','Volume'])
    #data = {'Time':[bar[0].t], 'Open':[bar[0].o], 'High':[bar[0].h], 'Low':[bar[0].l], 'Close':[bar[0].c], 'Volume':[bar[0].v]}
    #df = df.append(data,ignore_index=True)

    # df.append(getBar('MVIS','1Min',selectedTime))
    #hammerTimeTrading strategy is left uncalled until cronjob works
    #hammerTimeTrading(df,'MVIS')
    #print(df)
    #f = open("/Users/ryangould/Downloads/SP_DayTrading/test.txt", "a")
    #f.write(account.cash)
    #f.close()
