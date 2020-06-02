import dbConnector as db
import alpaca_trade_api as tradeapi
import redditScrape as rs
import datetime

BASE_URL = 'https://paper-api.alpaca.markets'
KEY_ID = 'PKXJ9PFWUR1PV0W4CR3Z'
SECRET_KEY = 'fQPmWsENWU7hrWlxoyGrPDsOOxehqkielyVs3bJ8'


if __name__ == '__main__':
    api = tradeapi.REST(KEY_ID, SECRET_KEY, BASE_URL)

    account = api.get_account()


    # Connect to the database
    connector = db.dbConnector()
    connection = connector.createConnection()

    #create scraper object to get symbols from redditScrape
    scraper = rs.Scraper()
    unscreened_stocks = scraper.unscreenedStocks()
    selectedTime = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1)
    #edit list of tuples to be a list of symbols
    symbols = [i[0] for i in unscreened_stocks]
    count = 0
    #iterate through symbols getting bar info for each symbol of last minute
    for i in symbols:
        bar = api.get_barset(symbols[count], '1Min', limit=1, after=selectedTime)
        barset = bar[symbols[count]]
        #print(barset)
        #print(type(barset))
        #id - symbol - high - low - open - close - volume - shareCount - timestamp - barType
        if barset != None and barset:
            connector.insertBar(symbols[count], barset[0].h, barset[0].l, barset[0].o, barset[0].c, barset[0].v, 1, 'barType', connection)
        count += 1
