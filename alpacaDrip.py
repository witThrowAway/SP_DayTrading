#!/usr/bin/python
import alpaca_trade_api as api
import datetime
import pandas as pd
import pymysql.cursors
import pymysql
import numpy as np

BASE_URL = 'https://paper-api.alpaca.markets'
KEY_ID = 'PKXJ9PFWUR1PV0W4CR3Z'
SECRET_KEY = 'fQPmWsENWU7hrWlxoyGrPDsOOxehqkielyVs3bJ8'

class Strategy:
    def isHammerBar(self, bar):
        if True == np.where(bar['open'] <= (bar['high'] - bar['high'] * (1/200)),True,False):
            if True == np.where(bar['open'] > bar['close'],True,False):
                if True == np.where(bar['low'] * 1.045 < bar['close'],True,False):
                    if True == np.where(bar['low'] != bar['high'], True, False):
                            return True
    def simpleMovingAverageAcrossTime(self, workingSet, start, end):
        sum = 0.0
        simpleMovingAverage = 0.0
        n = 0.0
        y = 0
        for x in workingSet[start:end]:
            sum += workingSet[y]['close']
            y += 1
        simpleMovingAverage = sum/5
        if workingSet[start]['close'] > workingSet[start+3]['close']  and workingSet[start+3]['close'] > workingSet[end]['close']:
            simpleMovingAverage = -simpleMovingAverage

        return simpleMovingAverage
    def backtestSMA(self, workingSet, start, end):
        sum = 0.0
        simpleMovingAverage = 0.0
        n = 0.0
        y = 0
        for x in workingSet[start:end]:
            sum += workingSet.iloc[y]['close']
            y += 1
        simpleMovingAverage = sum/5
        #if simpleMovingAverage < workingSet[start]:
        if workingSet.iloc[start]['close'] > workingSet.iloc[start+3]['close']  and workingSet.iloc[start+3]['close'] > workingSet.iloc[end]['close']:
            simpleMovingAverage = -simpleMovingAverage


        return simpleMovingAverage

    #function containing a complete strategy
    def hammerTimeTrading(self, sma, symbol, bar):
        #check if the current bar is a hammer and the last 5 bars were a negative moving average
        if self.isHammerBar(bar[0]) and sma < 0:
            #buy position at hammer (current bar)
            api.submit_order(
                symbol=symbol,
                side='buy',
                type='limit',
                qty='100',
                time_in_force='day',
                order_class='bracket',
                take_profit=dict(
                    limit_price=bar['close'] + .5,
                ),
                stop_loss=dict(
                    stop_price=bar['close'] - .5,
                )
            )
            print('ORDER SUBMITTED')

            return True
