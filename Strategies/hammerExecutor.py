import datetime
from datetime import time
import sys
from numpy import float as floaty

sys.path.append('/Users/ryan/IdeaProjects/SP_DayTrading/')

import dbConnector as db
import alpacaDrip as ad



if __name__ == "__main__":

        #start this strategy at 9:35 AM
        start_time = datetime.datetime.now()
        if datetime.datetime.now().time() > datetime.time(9,35) and datetime.datetime.now().time() <= datetime.time(16,1):
                # Connect to the database
                connector = db.dbConnector()
                connection = connector.createConnection()

                #create time window (5min intervals updated each minute)
                now = datetime.datetime.now()
                window = datetime.datetime.now() - datetime.timedelta(minutes=5)
                symbols = connector.getMentions(connection)
                strategy = ad.Strategy()
                sma = 0
                shares = 0
                takeProfitPercent = 1.04
                lossProfitPercent = .98
                buyClose = datetime.time(14,00)
                marketClose = datetime.time(15,30)
                alltrades = []

                takeProfit = floaty()
                lossProfit = floaty()
                for x in symbols[0:50]:
                    workingSet = connector.getBarsByTimeWindow(connection, window, now, x['symbol'])
                    cash = connector.getCash(connection,8)
                    cash = cash[0]['cash']
                    maxPosition = cash * .1
                    if len(workingSet) >= 5:
                        #print(workingSet)
                        currentBar = len(workingSet)-1
                        #print(workingSet[0]['close'])
                        sma = strategy.simpleMovingAverageAcrossTime(workingSet,0,currentBar)

                        currentPosition = connector.getPosition(connection, x['symbol'], 'hammer')
                        existingPosition = 0
                        #print(sma)
                        if len(currentPosition) == 0:
                            currentPosition = 0
                        else:
                            currentPosition = currentPosition[0]['position']
                            targets = connector.getLossProfitFromLastTradeOnSymbol(connection, x['symbol'], 'hammerBuy')
                            if targets:
                                takeProfit = targets[0]['takeProfit']
                                lossProfit = targets[0]['takeLoss']
                            existingPosition = 1

                        closePrice = workingSet[currentBar]['close']
                        shares = int(maxPosition / closePrice)
                        cashChange = shares * closePrice
                        prediction = strategy.predictOnHammer(workingSet)
                        if prediction == 1 and currentPosition != 1 and buyClose > workingSet[currentBar]['timestamp'].time() and cash > cashChange:
                                    print("-",cash)
                                    connector.subtractCash(connection, cashChange, 8)
                                    takeProfit = takeProfitPercent * closePrice
                                    lossProfit = lossProfitPercent * closePrice
                                    #if strategy.submitBuyOrder(x['symbol'], shares, closePrice):
                                    if existingPosition == 0:
                                            connector.insertPosition(connection,workingSet[currentBar]['symbol'], 'hammer')
                                    else:
                                        connector.modifyPosition(connection,workingSet[currentBar]['symbol'], 1, 'hammer')
                                    print("hammerBuy")
                                    connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, 'hammerBuy', connection,takeProfit,lossProfit)


                        if currentPosition == 1:
                                    print(currentPosition, " ",workingSet[currentBar]['symbol'], " ", workingSet[currentBar]['timestamp'].time())
                                    if closePrice >= takeProfit:
                                            print('hsell')
                                            uncleanShareCount = connector.getSharesFromLastTradeOnSymbol(connection, workingSet[currentBar]['symbol'], 'hammerBuy')
                                            shares = uncleanShareCount[0]['shareCount']
                                            cashChange = shares * closePrice
                                            #if strategy.submitSellOrder(x['symbol'], shares):
                                            connector.addCash(connection, cashChange, 8)
                                            connector.modifyPosition(connection,workingSet[currentBar]['symbol'],0,'hammer')
                                                #print("modifyPosition")
                                            connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, 'hammerSellAtTakeProfit', connection,0,0)

                                    elif closePrice <= lossProfit:
                                        print('hsell')
                                        uncleanShareCount = connector.getSharesFromLastTradeOnSymbol(connection, workingSet[currentBar]['symbol'], 'hammerBuy')
                                        shares = uncleanShareCount[0]['shareCount']
                                        cashChange = shares * closePrice
                                        #if strategy.submitSellOrder(x['symbol'], shares):
                                        connector.addCash(connection, cashChange, 8)
                                        connector.modifyPosition(connection,workingSet[currentBar]['symbol'],0,'hammer')
                                        #print("modifyPosition")
                                        connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, 'hammerSellAtLossStop', connection,0,0)


                                    elif buyClose <= workingSet[currentBar]['timestamp'].time() and closePrice >= (takeProfit * lossProfitPercent):
                                        print('hsell')
                                        uncleanShareCount = connector.getSharesFromLastTradeOnSymbol(connection, workingSet[currentBar]['symbol'], 'hammerBuy')
                                        shares = uncleanShareCount[0]['shareCount']
                                        cashChange = shares * closePrice
                                        #if strategy.submitSellOrder(x['symbol'], shares):
                                        connector.addCash(connection, cashChange, 8)
                                        connector.modifyPosition(connection,workingSet[currentBar]['symbol'],0,'hammer')
                                        connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, 'hammerSellAtBuyClose', connection, 0,0)

                                    elif marketClose <= workingSet[currentBar]['timestamp'].time():
                                        print('hsell')
                                        uncleanShareCount = connector.getSharesFromLastTradeOnSymbol(connection, workingSet[currentBar]['symbol'], 'hammerBuy')
                                        shares = uncleanShareCount[0]['shareCount']
                                        cashChange = shares * closePrice
                                        #if strategy.submitSellOrder(x['symbol'], shares):
                                        connector.addCash(connection, cashChange, 8)
                                        connector.modifyPosition(connection,workingSet[currentBar]['symbol'],0,'hammer')
                                        connector.insertTrade(workingSet[currentBar]['symbol'], workingSet[currentBar]['high'], workingSet[currentBar]['low'], workingSet[currentBar]['open'], workingSet[currentBar]['close'], workingSet[currentBar]['volume'], shares, 'hammerSellAtMarketClose', connection, 0,0)
        #print("hammer time taken:", (datetime.datetime.now() - start_time))
