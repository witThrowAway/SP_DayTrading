from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import sys

import backtrader as bt
import backtrader.feeds as btfeeds

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        #if the closing prcie is greater than the previous
        if self.dataclose[0] > self.dataclose[-1]:
            self.log("BUY BUY BUY")
            self.buy()


if __name__ == '__main__':


    datapath = "/Users/ryangould/Downloads/SP_DayTrading/datafeed.csv"
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
        volume=5
    )

    #print(modpath)
    print(datapath)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000.0)
    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('final value: %.2f' % cerebro.broker.getvalue())