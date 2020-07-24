#!/usr/bin/python
import alpaca_trade_api as tradeapi
import datetime
import pandas as pd
import pymysql.cursors
import pymysql
import numpy as np
import time

ALPACA_KEY_ID = 'PK3VZLXGJAE5FPVLWCOU'
ALPACA_SECRET_KEY = r'NtLnmeY6PtUpPXD2kGblhezLg/6f4lHqEcIqrR/3'

api = tradeapi.REST(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    base_url='https://paper-api.alpaca.markets'
)
class Strategy:
    def isHammerBar(self, bar):
        if True == np.where(bar['open'] <= bar['high'],True,False):
            if True == np.where(bar['open'] > bar['close'],True,False):
                if True == np.where(bar['low'] * 1.025 < bar['close'],True,False):
                        return True
        else:
            return False
    def simpleMovingAverageAcrossTime(self, workingSet, start, end):
        sum = 0.0
        simpleMovingAverage = 0.0
        for x in range(start,end+1):
            sum += workingSet[x]['close']
        simpleMovingAverage = sum/5
        if simpleMovingAverage < workingSet[start]['close']:
            simpleMovingAverage = -simpleMovingAverage

        return simpleMovingAverage
    def backtestSMA(self, workingSet, start, end):
        sum = 0.0
        simpleMovingAverage = 0.0
        for x in range(start,end):
            sum += workingSet.iloc[x]['close']
        simpleMovingAverage = sum/5
        if simpleMovingAverage < workingSet.iloc[start]['close']:
            simpleMovingAverage = -simpleMovingAverage
        return simpleMovingAverage

    def submitBuyOrder(self, symbol, shares, limitPrice):

            api.submit_order(
                symbol=symbol,
                side='buy',
                type='limit',
                qty=shares,
                time_in_force='day',
                limit_price= limitPrice,

            )
            time.sleep(4)
            currentOrders = api.list_orders()
            for order in currentOrders:
                if order.symbol == symbol and order.qty == shares:
                    print('Order not filled')
                    api.cancel_order(order.id)
                    return False

            return True
    def submitSellOrder(self,symbol,shares):
        api.submit_order(
            symbol=symbol,
            side='sell',
            type='market',
            qty=shares,
            time_in_force='gtc',
        )
        return True

    def calculateProfits(self, connector, connection, algo):
        buy = []
        sell = []

        trades = connector.getTradesAlgoAndDate(connection, algo + 'Buy', algo + 'SellAtTakeProfit', algo + 'SellAtBuyClose', algo + 'SellAtLossStop', algo + 'buy', algo + 'sell')
        changes = []
        for x in trades:
            tradeStr = x['tradeType']
            if tradeStr.find('Buy') != -1 or tradeStr.find('buy') != -1:
                buy.append((x['symbol'], x['close'], x['timestamp']))
            if tradeStr.find('Sell') != -1 or tradeStr.find('sell') != -1:
                sell.append((x['symbol'], x['close'], x['timestamp']))

        print(buy)
        print(sell)
        print(len(buy))
        print(len(sell))
        n1 = len(buy)-1
        n2 = len(sell)-1
        tradeCap = n2-1
        x = 0
        y = 0
        tradeCounter = 0

        while (n1 > 0 and n2 > 0) and tradeCounter < tradeCap:
            y += 1
            if buy[x][0] == sell[y][0]:
                change = sell[y][1] - buy[x][1]
                changes.append((change, sell[y][2]))
                buy.remove(buy[x])
                sell.remove(sell[y])
                n1 = len(buy)-1
                n2 = len(sell)-1
                x = 0
                y = 0
                tradeCounter+=1
            if y == n2:
                x += 1
                y = 0
            if x == n1:
                x = 0
                y = 0

        changes.sort(key = lambda x: x[1])
        return changes
