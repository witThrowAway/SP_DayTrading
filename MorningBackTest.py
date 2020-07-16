import alpaca_trade_api as tradeapi
import ta
import pandas as pd
import datetime
import numpy as np
from numpy import float as floaty

#Global Variables
ALPACA_KEY_ID = 'PK3VZLXGJAE5FPVLWCOU'
ALPACA_SECRET_KEY = r'NtLnmeY6PtUpPXD2kGblhezLg/6f4lHqEcIqrR/3'
SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

api = tradeapi.REST(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    base_url='https://paper-api.alpaca.markets/'
)

def Pythonstartrader(api, stock, from_time, to_time, cash):
    alltrades = []
    cash = floaty(cash)

    currentPosition = None
    barNumber = 0
    buyPrice = 0
    shares = 0
    takeProfitPercent = 1.04
    lossProfitPercent = .99
    maxPosition = cash * .05

    takeProfit = floaty()
    lossProfit = floaty()

    marketOpen = datetime.time(hour=9, minute=45, second=0, microsecond=0)
    buyClose = datetime.time(hour=11, minute=0, second=0, microsecond=0)

    df = api.polygon.historic_agg_v2(stock, 1, 'minute', _from=from_time, to=to_time).df


    while barNumber <= len(df) - 1:

        if (df.index[barNumber].time() > marketOpen and df.index[barNumber].time() < buyClose) or currentPosition:
            closePrice = df.iloc[barNumber]['close']

            three_bar =[df.iloc[barNumber-1]]

            set = [df.iloc[barNumber - 2], df.iloc[barNumber - 1], df.iloc[barNumber]]

            if isMorningStar(set):
                alltrades.append(str((df.index[barNumber])) + ' Buy at: ' + str(closePrice))
                buyPrice = df.iloc[barNumber]['close']
                shares = int(maxPosition / closePrice)
                cash = cash - shares * closePrice
                takeProfit = takeProfitPercent * buyPrice
                lossProfit = lossProfitPercent * buyPrice
                currentPosition = 1

            if currentPosition == 1:

                    if closePrice >= takeProfit:
                        if (buyPrice < closePrice):
                            alltrades.append(str((df.index[barNumber])) + ' Sell at: ' + str(closePrice))
                            cash += (shares * closePrice)
                            currentPosition = 0


                    elif closePrice <= lossProfit:
                        alltrades.append(str((df.index[barNumber])) + ' Sell at: ' + str(closePrice))
                        cash += (shares * closePrice)
                        currentPosition = 0

                    elif buyClose <= df.index[barNumber].time():
                        alltrades.append(str((df.index[barNumber])) + ' Sell at: ' + str(closePrice))
                        cash += (shares * closePrice)
                        currentPosition = 0


        barNumber+=1
    return alltrades,floaty(cash)

def isMorningStar(bar):


            if bar[0]['open'] > bar[1]['open'] and bar[2]['open'] < bar[1]['open']:

                if bar[0]['volume'] < bar[1]['volume'] and bar[2]['volume'] > bar[1]['volume']:

                    if bar[2]['volume'] >= (.95 * bar[1]['volume']):

                        if bar[0]['low'] >= bar[1]['low'] and bar[2]['low'] < bar[0]['low'] and bar[1]['low'] < bar[2]['low']:

                            return True



def algoStart(api, stocks, from_time, to_time, cash):
    positions = []
    cash = floaty(cash)

    for stock in stocks:
        alltrades, remaining = Pythonstartrader(api, stock, from_time, to_time, cash)
        profit = round((remaining - cash), 0)
        positions.append((stock, alltrades, profit))
    return positions, profit


if __name__ == '__main__':

    cash = floaty(25000)
    stocks = ['PLAY']
    from_time = '2020-06-15'
    to_time = '2020-06-19'
    profits = []
    positions, remaining = algoStart(api, stocks,from_time, to_time,cash )

    print(positions)
    print(remaining)