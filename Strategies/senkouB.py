import alpaca_trade_api as tradeapi
import ta
import pandas as pd
import time
import datetime
from numpy import float as floaty
import dbConnector as db
from Scrapers import finvizScrape

positionsOpen = []
cash = 0

api = tradeapi.REST(
    key_id='PKFVIO2UTE0RQCA10VY2',
    secret_key=r'UbQc/3SLmA5wv4EbesUh0t5dbUBdLAl/OtaEurrN',
    base_url='https://paper-api.alpaca.markets'
)


class position:
    def __init__(self, stock, currentPosition):
        self.symbol = stock
        self.currentPosition = currentPosition
        self.buyPrice = floaty()
        self.shares = 0
        self.takeProfit = floaty()
        self.lossProfit = floaty()
        self.closePrice = floaty()
        self.volume = int()
        self.high = floaty()
        self.low = floaty()
        self.open = floaty()

    def clearValues(self):
        self.symbol = self.symbol
        self.currentPosition = False
        self.buyPrice = floaty()
        self.shares = 0
        self.takeProfit = floaty()
        self.lossProfit = floaty()
        self.closePrice = floaty()
        self.volume = int()
        self.high = floaty()
        self.low = floaty()
        self.open = floaty()


def submitBuyOrder(stockObject, stockIndex):
    # Submit Order on Alpaca

    currentOrders = api.list_orders()
    for order in currentOrders:
        if order.symbol == stockObject.symbol:
            return False

    api.submit_order(
        symbol=stockObject.symbol,
        side='buy',
        type='limit',
        qty=stockObject.shares,
        time_in_force='day',
        limit_price=stockObject.buyPrice
    )

    time.sleep(4)
    currentOrders = api.list_orders()
    for order in currentOrders:
        if order.symbol == stockObject.symbol and order.qty == stockObject.shares:
            print('Order not filled')
            api.cancel_order(order.id)
            return False

    print('Bought ' + str(stockObject.symbol) + ' ' + str(stockObject.buyPrice))
    positionsOpen[stockIndex].currentPosition = 1
    connector.insertTrade(stockObject.symbol, floaty(stockObject.highPrice), floaty(stockObject.lowPrice), floaty(stockObject.openPrice),
                          floaty(stockObject.closePrice), int(positionsOpen[stockIndex].shares), int(stockObject.volume),
                          'none', 'senkouB_buy', connection)


    return True

def updateValues(stockIndex, closePrice, highPrice, lowPrice, openPrice, volume):
    positionsOpen[stockIndex].closePrice = closePrice
    positionsOpen[stockIndex].highPrice = highPrice
    positionsOpen[stockIndex].lowPrice = lowPrice
    positionsOpen[stockIndex].openPrice = openPrice
    positionsOpen[stockIndex].volume = volume

def submitSellOrder(stockObject, stockIndex):
    # Submit Order on Alpaca
    global cash

    print(stockObject.symbol + ' Sell at: ' + str(stockObject.closePrice))
    cash += (positionsOpen[stockIndex].shares * stockObject.closePrice)
    positionsOpen[stockIndex].currentPosition = 0

    api.submit_order(
        symbol=stockObject.symbol,
        side='sell',
        type='market',
        qty=stockObject.shares,
        time_in_force='gtc',
    )

    connector.insertTrade(stockObject.symbol, floaty(stockObject.highPrice), floaty(stockObject.lowPrice), floaty(stockObject.openPrice),
                          floaty(stockObject.closePrice),
                          int(positionsOpen[stockIndex].shares), int(stockObject.volume), 'none', 'senkouB_sell',
                          connection)

    positionsOpen[stockIndex].clearValues()


def algo(stock):
    global cash
    maxTrade = cash * .07

    # Add to list if it is not in it
    if not (any(x for x in positionsOpen if x.symbol == stock)):
        positionsOpen.append(position(stock, 0))

    stockIndex = 0

    for x in positionsOpen:
        if x.symbol == stock:
            break
        stockIndex = stockIndex + 1

    # Market variables
    marketOpen = datetime.time(hour=9, minute=30, second=0, microsecond=0)
    buyClose = datetime.time(hour=15, minute=30, second=0, microsecond=0)

    # Risk ratios
    takeProfitPercent = 1.07
    lossProfitPercent = .97

    try:
        df = api.polygon.historic_agg_v2(stock, 1, 'minute', _from=str(datetime.datetime.today()),
                                         to=str(datetime.datetime.today())).df
    except Exception as e:
        print(e)
        return False

    askPrice = round(api.polygon.last_quote(stock).askprice, 2)

    df.at[df.tail(1).index.item(), 'close'] = askPrice

    # Senkou Span B Calculation
    period52_high = df['high'].rolling(window=26).max()
    period52_low = df['low'].rolling(window=26).min()
    df['senkouB'] = ((period52_high + period52_low) / 2).shift(13)
    df['senkouB'] = df['senkouB'].fillna(df.iloc[1]['close'])
    df['volume'] = df['volume'].values.astype(floaty)


    # VWAP calculations
    df['vwap'] = ta.volume.VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'],
                                                      volume=df['volume'], n=1000, fillna=True).volume_weighted_average_price()
    # Volume is at least 50% the previous 20 minutes
    df['volume20avg'] = df['volume'].rolling(window=20).mean()
    df['volume20avg'] = df['volume20avg'].fillna(df.iloc[1]['volume'])


    #Assign all the variables we will need for the algo
    lastRow = (df.tail(1))
    lastRowTime = lastRow.index[0].time()
    closePrice = lastRow.iloc[-1]['close']
    highPrice = lastRow.iloc[-1]['high']
    lowPrice = lastRow.iloc[-1]['low']
    openPrice = lastRow.iloc[-1]['open']
    volume = (lastRow.iloc[-1]['volume'])
    volumeavg = (lastRow.iloc[-1]['volume20avg'])
    vwapPrice = (lastRow.iloc[-1]['vwap'])
    senkouPrice = (lastRow.iloc[-1]['senkouB'])

    if vwapPrice > senkouPrice: higherValue = vwapPrice

    #Make sure it has recenty crossed (last 5 mins)
    in_20 = False
    for index, row in df[['senkouB', 'vwap', 'close']].tail(5).iterrows():
        if row.close <= row.vwap or row.close <= row.senkouB:
            in_20 = True


    firstValue = df[['close']].tail(15).head(1).close[0]
    highestValue = df[['close']].tail(15).head(1).close[0]
    three_percent_gain = False
    #Make sure it has a gain of at least 3% in the last 15 minutes
    for index, row in df[['close']].tail(15).iterrows():
        if row.close > highestValue:
            highestValue = row.close
    if floaty(highestValue/firstValue) - 1.00 > .025:
        three_percent_gain = True


    try:
        if (lastRowTime > marketOpen):#and lastRowTime < buyClose):

            # Buy check ----------
            # first check if open position
            # Next check if volume is greater than 50% of 20 min moving average,
            # if current price is above the VWAP,
            # if the price crossed senkou and vwap within last 20 minutes
            # and current price is above Senkou B

            if  volume >= volumeavg/3.0 and closePrice > vwapPrice and in_20 and closePrice > senkouPrice and three_percent_gain and not positionsOpen[stockIndex].currentPosition:
                #print('Stock %s vwapPrice %s senkouPrice %s closePrice %s' % (stock, vwapPrice, senkouPrice, closePrice))
                updateValues(stockIndex, closePrice, highPrice, lowPrice, openPrice, volume)
                try:
                    if api.get_asset(stock).tradable:
                        positionsOpen[stockIndex].buyPrice = closePrice
                        positionsOpen[stockIndex].shares = int(maxTrade / askPrice)
                        cash = cash - (positionsOpen[stockIndex].shares * askPrice)
                        positionsOpen[stockIndex].takeProfit = takeProfitPercent * askPrice
                        positionsOpen[stockIndex].lossProfit = lossProfitPercent * askPrice
                        submitBuyOrder(positionsOpen[stockIndex], stockIndex)

                except Exception as e:
                    print(e)
                    pass

            #Sell check ---------
            #First check if open position
            elif (positionsOpen[stockIndex].currentPosition):

                #Check if we have hit our take profit mark
                if closePrice >= positionsOpen[stockIndex].takeProfit:
                    updateValues(stockIndex, closePrice, highPrice, lowPrice, openPrice, volume)
                    submitSellOrder(positionsOpen[stockIndex], stockIndex)
                elif closePrice <= positionsOpen[stockIndex].lossProfit:
                    updateValues(stockIndex, closePrice, highPrice, lowPrice, openPrice, volume)
                    submitSellOrder(positionsOpen[stockIndex], stockIndex)
                elif buyClose <= lastRowTime:
                    updateValues(stockIndex, closePrice, highPrice, lowPrice, openPrice, volume)
                    submitSellOrder(positionsOpen[stockIndex], stockIndex)


    except Exception as e:
        print(str(e.args))


if __name__ == '__main__':

    connector = db.dbConnector()
    connection = connector.createConnection()
    allStocks = finvizScrape.scrape()

    while True:
        for stock in allStocks:
            account = (api.get_account())
            cash = floaty(account.cash)
            if float(stock.changePercent) >= 3:
                print(stock.symbol)
                algo(stock.symbol)
        for p in positionsOpen:
            if p.currentPosition == 1:
                print(p.symbol + ' ' + str(p.buyPrice) + ' ' + str(p.shares))
        print('Waiting. . .')
        time.sleep(10)
