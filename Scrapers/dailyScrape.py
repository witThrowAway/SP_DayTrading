import sys
import pandas as pd
import datetime
import alpaca_trade_api as tradeapi

sys.path.append('/Users/ryan/IdeaProjects/SP_DayTrading/')
import dbConnector as db
from Scrapers import redditScraper as rs
from Scrapers import marketwatchScraper as ms



if __name__ == '__main__':
    #initialize API information
    ALPACA_KEY_ID = 'PKD6W26XBA1JGWOSJSU0'
    ALPACA_SECRET_KEY = r'ysaezMtOX8sUghmR534ZGzEXzCTVpkDt26BEIY8e'
    APCA_RETRY_MAX=1
    api = tradeapi.REST(
        key_id=ALPACA_KEY_ID,
        secret_key=ALPACA_SECRET_KEY,
        base_url='https://paper-api.alpaca.markets'
    )

    # Connect to the database
    connector = db.dbConnector()
    connection = connector.createConnection()

    #get stocks from reddit
    redditScraperStocks = rs.scrape()
    symbols = [i[0] for i in redditScraperStocks]
    print(symbols)

    #marketWatch
    marketWatchObjects = ms.scrape()
    marketWatchStocks = []
    for stockObject in marketWatchObjects:
        marketWatchStocks.append(stockObject.symbol)
    print(marketWatchStocks)

    for x in marketWatchStocks[1:75]:
        tryCounter = 0
        asset = None
        while asset is None and tryCounter < 5:
            asset = api.get_asset(x)
            tryCounter += 1
        if asset.tradeable:
            connector.insertMention(x,connection)
    for x in symbols[1:75]:
        tryCounter = 0
        asset = None
        while asset is None and tryCounter < 5:
            asset = api.get_asset(x)
            tryCounter += 1
        if asset.tradeable:
            connector.insertMention(x,connection)
    print("daily scrape executed")
