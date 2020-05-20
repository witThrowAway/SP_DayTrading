from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import sys

import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import redditScrape as rs

class TestStrategy(bt.Strategy):
    #scraper = 0 #???? make this param a redditScrape object??????

    def __init__(self, scraper):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.scraper = scraper
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        df = pd.read_csv(r"C:\Users\n3oera\PycharmProjects\SP_DayTrading\datafeed.csv")
        hammertimes = self.scraper.areThereBearishHammerTimes(df)
        simpleMovingAverage = self.scraper.simpleMovingAverage(-5,0,self.data)
        y = 0
        for x in hammertimes:
            y = y + 1
            #if the closing prcie is greater than the previous
            if self.dataclose[0] == hammertimes[y] and simpleMovingAverage < 0:
                self.log("BUY BUY BUY")
                self.buy()


if __name__ == '__main__':


    datapath = r"C:\Users\n3oera\PycharmProjects\SP_DayTrading\datafeed.csv"
    data = btfeeds.GenericCSVData(
        dataname=datapath,
        #A -1 value signifies value isnt present
        time=-1,
        openinterest=-1,
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=50.

    )

    #print(modpath)
    print(datapath)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000.0)
    cerebro.adddata(data)
    #scraper = rs.Scraper()

    cerebro.addstrategy(TestStrategy)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('final value: %.2f' % cerebro.broker.getvalue())