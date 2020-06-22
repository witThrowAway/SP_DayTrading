import alpaca_trade_api as tradeapi
import ta
import pandas as pd
import datetime
from numpy import float as floaty

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

def algoStart(api, stocks, from_time, to_time, cash):
    positions = []
    cash = floaty(cash)


    for stock in stocks:
        alltrades, remaining = bband_rsi_algo (api, stock, from_time, to_time, cash)
        profit = round((remaining - cash), 0)
        positions.append((stock, alltrades, profit))
    return positions