import alpaca_trade_api as tradeapi
import ta
import pandas as pd
import datetime
from numpy import float as floaty
from numpy import nan
import alpacaDrip as ad
import dbConnector as db

pd.options.display.max_columns = None
pd.options.display.max_rows = None

def senkouB(api, stock, from_time, to_time, cash):
    alltrades = []
    cash = floaty(cash)

    marketOpen = datetime.time(hour=9, minute=35, second=0, microsecond=0)
    buyClose = datetime.time(hour=15, minute=00, second=0, microsecond=0)

    currentPosition = 0
    barNumber = 2
    shares = 0
    takeProfitPercent = 1.08
    lossProfitPercent = .96
    maxPosition = cash * .3

    takeProfit = floaty()
    lossProfit = floaty()

    try:
        df = api.polygon.historic_agg_v2(stock, 1, 'minute', _from=from_time, to=to_time).df
    except Exception as e:
        print('Invalid Stock')
        return False

    # Senkou Span B Calculation
    period52_high = df['high'].rolling(window=26).max()
    period52_low = df['low'].rolling(window=26).min()
    df['senkouB'] = ((period52_high + period52_low) / 2).shift(13)
    df['senkouB'] = df['senkouB'].fillna(df.iloc[0]['close'])
    df['volume'] = df['volume'].values.astype(floaty)

    # VWAP calculations
    df['vwap'] = ta.volume.VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'],
                                                      volume=df['volume'], n=1000,
                                                      fillna=True).volume_weighted_average_price()

    # Volume is at least 50% the previous 20 minutes
    df['volume20avg'] = df['volume'].rolling(window=20).mean()
    df['volume20avg'] = df['volume20avg'].fillna(df.iloc[0]['volume'])




    try:
        while barNumber <= len(df) - 1:

            # Assign all the variables we will need for the algo
            df2 = df.head(barNumber)
            lastRow = (df2.tail(1))
            closePrice = lastRow.iloc[0]['close']
            volume = lastRow.iloc[0]['volume']
            volumeavg = (lastRow.iloc[0]['volume20avg'])
            vwapPrice = (lastRow.iloc[0]['vwap'])
            senkouPrice = (lastRow.iloc[0]['senkouB'])

            if vwapPrice > senkouPrice: higherValue = vwapPrice

            if (df2.index[-1].time() > marketOpen and df2.index[-1].time() < buyClose or currentPosition):
                # Make sure it has recenty crossed (last 20 mins)

                in_20 = False

                for index, row in df2[['senkouB', 'vwap', 'close']].head(barNumber).tail(5).iterrows():
                    if row.close <= row.vwap or row.close <= row.senkouB:
                        in_20 = True

                print(df2.index[-1].time())
                print(closePrice)
                print(senkouPrice)

                firstValue = df2[['close']].tail(15).head(1).close[0]
                highestValue = df2[['close']].tail(15).head(1).close[0]
                three_percent_gain = False
                # Make sure it has a gain of at least 3% in the last 15 minutes
                for index, row in df2[['close']].tail(15).iterrows():
                    if row.close > highestValue:
                        highestValue = row.close
                if floaty(highestValue / firstValue) - 1.00 > .025:
                    three_percent_gain = True

                if not currentPosition and volume >= volumeavg / 3.0 and closePrice > vwapPrice and in_20 and closePrice > senkouPrice and three_percent_gain:
                    alltrades.append(str((df2.index[-1])) + ' Buy at: ' + str(closePrice))
                    shares = int(maxPosition / closePrice)
                    cash = cash - shares * closePrice
                    takeProfit = takeProfitPercent * closePrice
                    lossProfit = lossProfitPercent * closePrice
                    currentPosition = 1

                # sell check
                elif (currentPosition):
                    if closePrice >= takeProfit:
                        alltrades.append(str((df2.index[-1])) + ' Sell at: ' + str(closePrice))
                        cash += (shares * closePrice)
                        currentPosition = 0

                    elif closePrice <= vwapPrice - .05:
                        alltrades.append(str((df2.index[-1])) + ' Sell at: ' + str(closePrice))
                        cash += (shares * closePrice)
                        currentPosition = 0



                    elif closePrice <= lossProfit:
                        alltrades.append(str((df2.index[-1])) + ' Sell at: ' + str(closePrice))
                        cash += (shares * closePrice)
                        currentPosition = 0

                    elif buyClose <= df2.index[-1].time():
                        alltrades.append(str((df2.index[-1])) + ' Sell at: ' + str(closePrice))
                        cash += (shares * closePrice)
                        currentPosition = 0

            barNumber += 1


    except Exception as e:
        print(str(e.args))

    return alltrades, floaty(cash)


def bband_rsi_algo(api, stock, from_time, to_time, cash):
    alltrades = []
    cash = floaty(cash)

    marketOpen = datetime.time(hour=9, minute=45, second=0, microsecond=0)
    buyClose = datetime.time(hour=14, minute=0, second=0, microsecond=0)

    currentPosition = None
    barNumber = 0
    buyPrice = 0
    shares = 0
    takeProfitPercent = 1.03
    lossProfitPercent = .99
    maxPosition = cash * .05

    takeProfit = floaty()
    lossProfit = floaty()

    df = api.polygon.historic_agg_v2(stock, 1, 'minute', _from=from_time, to=to_time).df

    # BBANDS calculations
    indicator_bb = ta.volatility.BollingerBands(close=df["close"], n=20, ndev=1.5)
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()
    # RSI calculations
    df['RSI'] = ta.momentum.RSIIndicator(close=df["close"], n=14).rsi()

    try:

        while barNumber <= len(df) - 1:

            # Check if moving average is positive for the last 10 minutes

            if (df.index[barNumber].time() > marketOpen and df.index[barNumber].time() < buyClose) or currentPosition:

                closePrice = df.iloc[barNumber]['close']

                # Make sure BBAND Values and RSI values are not NaN
                if not (pd.isnull((df.iloc[barNumber]['bb_bbm']))):

                    # buy check
                    if not currentPosition:
                        if closePrice <= df.iloc[barNumber][
                            'bb_bbl'] * 1.00:  # see if close price is less than or equal too lower band

                            if round(df.iloc[barNumber]['RSI']) <= 34:  # make sure RSI indicates oversold position
                                alltrades.append(str((df.index[barNumber])) + ' Buy at: ' + str(closePrice))
                                buyPrice = df.iloc[barNumber]['close']
                                shares = int(maxPosition / closePrice)
                                cash = cash - shares * closePrice
                                takeProfit = takeProfitPercent * buyPrice
                                lossProfit = lossProfitPercent * buyPrice
                                currentPosition = 1

                    # sell check
                    elif (currentPosition and closePrice >= df.iloc[barNumber]['bb_bbh'] * .90) or (
                            currentPosition and round(df.iloc[barNumber]['RSI']) >= 60) or (
                            currentPosition and closePrice <= lossProfit):

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

            barNumber += 1


    except Exception as e:
        print(str(e.args))

    return alltrades, floaty(cash)


def hammer_algo(api, stock, from_time, to_time, cash):
    alltrades = []
    cash = floaty(cash)

    marketOpen = datetime.time(hour=9, minute=40, second=0, microsecond=0)
    buyClose = datetime.time(hour=12, minute=0, second=0, microsecond=0)

    currentPosition = None
    barNumber = 1
    buyPrice = 0
    shares = 0
    takeProfitPercent = 1.06
    lossProfitPercent = .96
    maxPosition = cash * .1

    takeProfit = floaty()
    lossProfit = floaty()

    df = api.polygon.historic_agg_v2(stock, 1, 'minute', _from=from_time, to=to_time).df

    strategy = ad.Strategy()
    try:
        while barNumber <= len(df) - 1:
            if (df.index[barNumber].time() > marketOpen and df.index[barNumber].time() < buyClose) or currentPosition:
                if barNumber > 5:
                    closePrice = df.iloc[barNumber]['close']
                    start = barNumber - 5
                    sma = strategy.backtestSMA(df, start, barNumber)

                    if strategy.isHammerBar(df.iloc[barNumber]) and sma < 0:
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
            barNumber += 1

    except Exception as e:
        print(str(e.args))

    return alltrades, floaty(cash)


def morningstar_algo(api, stock, from_time, to_time, cash):
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
    buyClose = datetime.time(hour=12, minute=0, second=0, microsecond=0)

    df = api.polygon.historic_agg_v2(stock, 1, 'minute', _from=from_time, to=to_time).df

    while barNumber <= len(df) - 1:

        if (df.index[barNumber].time() > marketOpen and df.index[barNumber].time() < buyClose) or currentPosition:
            closePrice = df.iloc[barNumber]['close']

            three_bar = [df.iloc[barNumber - 1]]

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

        barNumber += 1
    return alltrades, floaty(cash)


def isMorningStar(bar):
    if bar[0]['open'] > bar[1]['open'] and bar[2]['open'] < bar[1]['open']:

        if bar[0]['volume'] < bar[1]['volume'] and bar[2]['volume'] > bar[1]['volume']:

            if bar[2]['volume'] >= (.95 * bar[1]['volume']):

                if bar[0]['low'] >= bar[1]['low'] and bar[2]['low'] < bar[0]['low'] and bar[1]['low'] < bar[2]['low']:
                    return True


def algoStart(api, stocks, from_time, to_time, cash, strat):
    positions = []
    cash = floaty(cash)

    if strat == 'bband_rsi_algo':
        for stock in stocks:
            alltrades, remaining = bband_rsi_algo(api, stock, from_time, to_time, cash)
            profit = round((remaining - cash), 0)
            positions.append((stock, alltrades, profit))
    if strat == 'hammer':
        for stock in stocks:
            alltrades, remaining = hammer_algo(api, stock, from_time, to_time, cash)
            profit = round((remaining - cash), 0)
            positions.append((stock, alltrades, profit))
    if strat == 'morningStar':
        for stock in stocks:
            alltrades, remaining = morningstar_algo(api, stock, from_time, to_time, cash)
            profit = round((remaining - cash), 0)
            positions.append((stock, alltrades, profit))
    if strat == 'senkouB':
        for stock in stocks:
            try:
                alltrades, remaining = senkouB(api, stock, from_time, to_time, cash)
                profit = round((remaining - cash), 0)
                positions.append((stock, alltrades, profit))
            except Exception as e:
                pass

    return positions
