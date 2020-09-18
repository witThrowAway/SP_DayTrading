import dbConnector as db
import backtesting as bt
import alpaca_trade_api as tradeapi
import csv
from numpy import float as floaty


ALPACA_KEY_ID = 'PK3VZLXGJAE5FPVLWCOU'
ALPACA_SECRET_KEY = r'NtLnmeY6PtUpPXD2kGblhezLg/6f4lHqEcIqrR/3'

api = tradeapi.REST(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    base_url='https://paper-api.alpaca.markets'
)

if __name__ == "__main__":
    fromTime = "06-01-2017"
    toTime = "06-30-2017"

    connector = db.dbConnector()
    connection = connector.createConnection()
    symbols = connector.getAllDistinctMentions(connection)
    symbols = symbols[0:700]
    print(len(symbols))
    stocks = []
    takeProfit = 1.03
    takeLoss = .985
    filename = "/Users/ryangould/Desktop/hammerTradeTrainData.csv"
    fields = ["takeLoss", "takeProfit", "SMA", "tailLength", "volume", "hourOfBuy","minuteOfBuy", "profitable"]
    for x in symbols:
        stocks.append(x['symbol'])
    positions = bt.algoStart(api,stocks,fromTime,toTime, 25000)
    #print(positions)
    trades = []
    for x in positions:
        if x[2] != 0.0:
            trades.append(x)
    csvRows = []
    row = []
    #print(trades)
    for x in trades:
        row.append(takeLoss)
        row.append(takeProfit)
        row.append(x[3][1])
        row.append(floaty(x[3][0]['close']) - floaty(x[3][0]['low']))
        row.append(floaty(x[3][0]['volume']))
        row.append(x[1][0][11:13])
        row.append(x[1][0][14:16])
        if x[2] > 0:
            row.append(1)
        else:
            row.append(0)
        csvRows.append(row)
        row = []
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        #csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(csvRows)