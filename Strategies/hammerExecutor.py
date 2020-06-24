import datetime
import time
import sys
from numpy import float as floaty

sys.path.append('/home/trade/Desktop/SP_DayTrading/')

import dbConnector as db
import alpacaDrip as ad



if __name__ == "__main__":

    #start this strategy at 9:35 AM
        if datetime.datetime.now().time() > datetime.time(9,35) and datetime.datetime.now().time() < datetime.time(12,00):
            # Connect to the database
            connector = db.dbConnector()
            connection = connector.createConnection()

            #create time window (5min intervals updated each minute)
            now = datetime.datetime.now()
            window = datetime.datetime.now() - datetime.timedelta(minutes=5)
            symbols = connector.getMentions(connection)
            strategy = ad.Strategy()
            ############ make value dynamic
            cash = 25000
            ############
            sma = 0
            #barNumber = 0
            currentPosition = None
            buyPrice = 0
            shares = 0
            takeProfitPercent = 1.03
            lossProfitPercent = .97
            maxPosition = cash * .1
            buyClose = datetime.time(hour=12, minute=0, second=0, microsecond=0)
            alltrades = []

            takeProfit = floaty()
            lossProfit = floaty()
            for x in symbols:
                workingSet = connector.getBarsByTimeWindow(connection, window, now, x['symbol'])
                currentBar = len(workingSet)-1
                barNumber = 0
                if len(workingSet) == 5:
                    for x in workingSet:
                        print(x)
                        closePrice = workingSet[barNumber]['close']
                        sma = strategy.simpleMovingAverageAcrossTime(workingSet,0,currentBar)
                        if strategy.isHammerBar(workingSet[barNumber]) and sma < 0:
                            alltrades.append(str((x[barNumber])) + ' Buy at: ' + str(closePrice))
                            buyPrice = x[barNumber]['close']
                            shares = int(maxPosition / closePrice)
                            cash = cash - shares * closePrice
                            takeProfit = takeProfitPercent * buyPrice
                            lossProfit = lossProfitPercent * buyPrice
                            currentPosition = 1
                            connector.insertTrade(x['symbol'], x['high'], x['low'], x['open'], x['close'], x['volume'], 0, x['barType'], 'hammerBuy', connection)


                    if currentPosition == 1:
                            if closePrice >= takeProfit:
                                if (buyPrice < closePrice):
                                    alltrades.append(str((x[barNumber])) + ' Sell at: ' + str(closePrice))
                                    cash += (shares * closePrice)
                                    currentPosition = 0


                            elif closePrice <= lossProfit:
                                alltrades.append(str((x[barNumber])) + ' Sell at: ' + str(closePrice))
                                cash += (shares * closePrice)
                                currentPosition = 0

                            elif buyClose <= x[barNumber]['timestamp'].time():
                                alltrades.append(str((df.index[barNumber])) + ' Sell at: ' + str(closePrice))
                                cash += (shares * closePrice)
                                currentPosition = 0
                                connector.insertTrade(x['symbol'], x['high'], x['low'], x['open'], x['close'], x['volume'], 0, x['barType'], 'hammerSell', connection)
                barNumber += 1

