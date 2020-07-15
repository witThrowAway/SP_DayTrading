import dbConnector as db
import alpaca_trade_api as tradeapi
from Scrapers import redditScraper as rs
import datetime
import alpacaDrip as ad
import pandas as pd
from numpy import float as floaty


if __name__ == '__main__':

    start = datetime.datetime.now()
    if datetime.datetime.now().time() > datetime.time(9,30):
        #initialize API information
        ALPACA_KEY_ID = 'PK3VZLXGJAE5FPVLWCOU'
        ALPACA_SECRET_KEY = r'NtLnmeY6PtUpPXD2kGblhezLg/6f4lHqEcIqrR/3'

        api = tradeapi.REST(
            key_id=ALPACA_KEY_ID,
            secret_key=ALPACA_SECRET_KEY,
            base_url='https://paper-api.alpaca.markets'
        )

        # Connect to the database
        connector = db.dbConnector()
        connection = connector.createConnection()

        #Create time window to make api call for
        now = datetime.datetime.now()
        window = datetime.datetime.now() - datetime.timedelta(minutes=1)

        unscreened_stocks = connector.getMentions(connection)
        count = 0
        barType = 'barType'
        strategy = ad.Strategy()
        # iterate through symbols getting bar info for each symbol of last minute
        for x in unscreened_stocks:
            # bar = api.get_barset(symbols[count], '1Min', limit=1, after=selectedTime)
            df = pd.DataFrame()
            tryCounter = 0
            # check if df has a value to account for API response time
            while df.empty and tryCounter < 10:
                df = api.polygon.historic_agg_v2(unscreened_stocks[count]["symbol"], 1, 'minute', limit=1,
                                             _from=str(window), to=str(now)).df
                tryCounter +=1
            count += 1
            if not df.empty:
                if strategy.isHammerBar(df):
                    barType = 'hammer'
                # symbol - high - low - open - close - volume - shareCount - timestamp - barType
                try:
                    connector.insertBar(unscreened_stocks[count]["symbol"], floaty(df['high']), floaty(df['low']), floaty(df['open']),
                                floaty(df['close']), floaty(df['volume']), 1, barType, connection)
                except Exception as e:
                    print(str(e))
