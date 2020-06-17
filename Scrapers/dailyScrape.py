#from Desktop.SP_DayTrading
import dbConnector as db
import redditScraper as rs
import stocktwitScraper as st
import marketwatchScraper as ms



if __name__ == '__main__':

    # Connect to the database
    connector = db.dbConnector()
    connection = connector.createConnection()

    #get stocks from reddit
    redditScraperStocks = rs.scrape()
    symbols = [i[0] for i in redditScraperStocks]

    #marketWatch
    marketWatchObjects = ms.scrape()
    marketWatchStocks = []
    for stockObject in marketWatchObjects:
        marketWatchStocks.append(stockObject.symbol)

    for x in marketWatchStocks[1:75]:
        connector.insertMention(x,connection)
    for x in symbols[1:75]:
        connector.insertMention(x,connection)
