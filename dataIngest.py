import dbConnector as db
import alpaca_trade_api as tradeapi
from Scrapers import redditScraper as rs
import datetime
import alpacaDrip as ad
import time
from numpy import float as floaty


if __name__ == '__main__':


    if datetime.datetime.now().time() > datetime.time(9,30):
        #initialize API information
        api = tradeapi.REST(
            key_id='AKI81T1TR0P0KOFHGE9K',
            secret_key=r'6BsKrTdP0WdXSARbufPFV7hVjtwoYGDAx/3ZG9VK',
            base_url='https://paper-api.alpaca.markets'
        )

        # Connect to the database
        connector = db.dbConnector()
        connection = connector.createConnection()

        #create scraper object to get symbols from redditScrape
        selectedTime = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1)
        unscreened_stocks = connector.getMentions(connection)
        print(unscreened_stocks)
        symbols = []
        count = 0
        for x in unscreened_stocks:
            symbols.append(unscreened_stocks[count]["symbol"])
            count +=1
        count = 0
        barType = 'barType'
        strategy = ad.Strategy()
        millis = int(round(time.time() * 1000))
        #iterate through symbols getting bar info for each symbol of last minute
        for i in symbols:
            #bar = api.get_barset(symbols[count], '1Min', limit=1, after=selectedTime)
            df = api.polygon.historic_agg_v2(symbols[count], 1, 'minute' ,limit=1, _from=millis-120000, to=millis).df
            #check if barset has a value to account for API response time
            if not df.empty:
                #print(type(df['high']))
                if strategy.isHammerBar(df):
                    barType = 'hammer'
                #symbol - high - low - open - close - volume - shareCount - timestamp - barType
                try:
                    print(df)
                    connector.insertBar(symbols[count], floaty(df['high']), floaty(df['low']), floaty(df['open']),


                                        floaty(df['close']), floaty(df['volume']), 1, barType, connection)
                except Exception as e:
                    print(str(e))
            count += 1
