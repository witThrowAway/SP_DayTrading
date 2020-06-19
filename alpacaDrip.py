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
        print(bar)
        if True == np.where(bar['open'] <= (bar['high'] - bar['high'] * (1/200)),True,False):
            if True == np.where(bar['open'] > bar['close'],True,False):
                if True == np.where(bar['low'] * 1.025 < bar['close'],True,False):
                    return True
    def simpleMovingAverageAcrossTime(self, workingSet):
        sum = 0.0
        simpleMovingAverage = 0.0
        n = 0.0
        y = 0
        for x in workingSet[0:4]:
            sum += workingSet[y]['close']
            y += 1
        simpleMovingAverage = sum/5
        if workingSet[0]['close'] > workingSet[3]['close']  and workingSet[3]['close'] > workingSet[4]['close']:
            simpleMovingAverage = -simpleMovingAverage

        return simpleMovingAverage

    #function containing a complete strategy
    def hammerTimeTrading(self, sma, symbol, bar):
        #check if the current bar is a hammer and the last 5 bars were a negative moving average
        if bar[0]['barType'] == 'hammer' and sma < 0:
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
        #if we have an order and pice > 3% or < 1% of buy in
            #sell 
        else:
            return False
