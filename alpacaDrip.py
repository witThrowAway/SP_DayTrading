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
    def isHammerBar(self, bar):
        if bar[0].o <= (bar[0].h - bar[0].h * (1/200)):
            if bar[0].o > bar[0].c:
                if bar[0].l * 1.025 < bar[0].c:
                    return True
    def simpleMovingAverageAcrossTime(self, workingSet):
        sum = 0.0
        simpleMovingAverage = 0.0
        n = 0.0
        y = 0
        for x in workingSet[0:5]:
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

        return True
