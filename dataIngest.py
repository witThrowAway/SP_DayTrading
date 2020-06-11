import dbConnector as db
import alpaca_trade_api as tradeapi
from Scrapers import redditScraper as rs
import datetime
import alpacaDrip as ad



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
        unscreened_stocks = rs.scrape()
        selectedTime = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1)
        #edit list of tuples to be a list of symbols
        symbols = [i[0] for i in unscreened_stocks]
        count = 0
        barType = 'barType'
        strategy = ad.Strategy()

        #iterate through symbols getting bar info for each symbol of last minute
        for i in symbols:
            bar = api.get_barset(symbols[count], '1Min', limit=1, after=selectedTime)
            barset = bar[symbols[count]]
            #check if barset has a value to account for API response time
            if barset != None and barset:
                if strategy.isHammerBar(barset):
                    barType = 'hammer'
                #symbol - high - low - open - close - volume - shareCount - timestamp - barType
                connector.insertBar(symbols[count], barset[0].h, barset[0].l, barset[0].o, barset[0].c, barset[0].v, 1, barType, connection)
            count += 1
