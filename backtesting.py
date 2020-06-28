import alpaca_trade_api as tradeapi
import ta
import pandas as pd
import datetime
from numpy import float as floaty
import alpacaDrip as ad
import dbConnector as db

#Global Variables
ALPACA_KEY_ID = 'PKKJ09PTT163PO3V428W'
ALPACA_SECRET_KEY = r'kp0o8PWbO/XP1saBZRk98UDK2eQcr6Nacai219NR'
SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

api = tradeapi.REST(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    base_url='https://paper-api.alpaca.markets'
)

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
def backTestHammer(api, stock, from_time, to_time, cash):
    alltrades = []
    cash = floaty(cash)

    marketOpen = datetime.time(hour=9, minute=40, second=0, microsecond=0)
    buyClose = datetime.time(hour=12, minute=0, second=0, microsecond=0)

    currentPosition = None
    barNumber = 1
    buyPrice = 0
    shares = 0
    takeProfitPercent = 1.06
    lossProfitPercent = .97
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


def algoStart(api, stocks, from_time, to_time, cash):
    positions = []
    cash = floaty(cash)

    for stock in stocks:
        alltrades, remaining = backTestHammer(api, stock, from_time, to_time, cash)
        #bband_rsi_algo (api, stock, from_time, to_time, cash)
        profit = round((remaining - cash), 0)
        positions.append((stock, alltrades, profit))
    return positions

if __name__ == '__main__':
    positions = []
    cash = floaty(25000)
    stocks = ['MCF', 'ANTE', 'ORN', 'MOHO', 'HTBX', 'OTLK', 'IGC', 'WATER',
              'AUTO', 'MEIP', 'CPHI','NTZ', 'SAMAW', 'PIRIS', 'VXRT', 'TAOP', 'JAGX', 'ITP', 'DXF', 'CBAT',
              'PETZ', 'LMFA', 'BYFC', 'SNSS', 'CARV', 'NVFY', 'NTN']
    stocks2 = []
    stocks1 = ['PETZ', 'LMFA', 'BYFC', 'SNSS', 'CARV', 'NVFY', 'NTN']
    from_time = '2020-06-24'
    to_time = '2020-06-25'
    connector = db.dbConnector()
    connection = connector.createConnection()
    symbols = connector.getMentions(connection)
    for x in symbols:
        stocks2.append(x['symbol'])
    profits = []
    for stock in stocks2:
        alltrades, remaining = backTestHammer(api, stock, from_time, to_time, cash)
        #bband_rsi_algo (api, stock, from_time, to_time, cash)
        profit = round((remaining - cash), 0)
        profits.append(profit)
        positions.append((stock, alltrades, profit))

    print(positions)
    print(profits)
