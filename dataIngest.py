import dbConnector as db
import alpaca_trade_api as tradeapi
import datetime
import alpacaDrip as ad
import pandas as pd
from numpy import float as floaty


if __name__ == '__main__':

    start = datetime.datetime.now()

    if datetime.datetime.now().time() > datetime.time(9,30):
        #initialize API information
        ALPACA_KEY_ID = 'PKD6W26XBA1JGWOSJSU0'
        ALPACA_SECRET_KEY = r'ysaezMtOX8sUghmR534ZGzEXzCTVpkDt26BEIY8e'
        APCA_RETRY_MAX=0
        api = tradeapi.REST(
            key_id=ALPACA_KEY_ID,
            secret_key=ALPACA_SECRET_KEY,
            base_url='https://paper-api.alpaca.markets'
        )

        # Connect to the database
        connector = db.dbConnector()
        connection = connector.createConnection()

        #Create time window to make api call for
        window = datetime.datetime.now() - datetime.timedelta(minutes=1)
        unscreened_stocks = connector.getMentions(connection)
        strategy = ad.Strategy()
        aggregateData = []
        # iterate through symbols getting bar info for each symbol of last minute
        for x in unscreened_stocks[0:len(unscreened_stocks)-1]:
            df = pd.DataFrame()
            tryCounter = 0
            data = []
            # check if df has a value to account for API response time
            while df.empty and tryCounter < 5:
                df = api.get_barset(x["symbol"], '1Min', limit=1, after=window).df
                tryCounter +=1
            if not df.empty:
                data.append(x['symbol'])
                data.append(floaty(df.iloc[0][0]))
                data.append(floaty(df.iloc[0][1]))
                data.append(floaty(df.iloc[0][2]))
                data.append(floaty(df.iloc[0][3]))
                data.append(floaty(df.iloc[0][4]))
                data.append(window)
                aggregateData.append(data)
    connector.insertBars(aggregateData,connection)

    print("--- %s seconds ---" % (datetime.datetime.now() - start))
