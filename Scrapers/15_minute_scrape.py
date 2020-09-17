import sys
sys.path.append('/Users/ryan/IdeaProjects/SP_DayTrading/')
import dbConnector as db
from Scrapers import marketwatchScraper as ms


if __name__ == '__main__':

    # Connect to the database
    connector = db.dbConnector()
    connection = connector.createConnection()

    connector.purgeMarketWatchDB(connection)

    Mobjects = ms.scrape()

    for tmp in Mobjects:
        if tmp.changePercent < 6 or tmp.changePercent > 25:
            Mobjects.remove(tmp)


    for mStock in Mobjects:
        connector.insertMarketWatchObject(mStock.symbol, mStock.price, mStock.change, mStock.changePercent, mStock.volume, connection)


