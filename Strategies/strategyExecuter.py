import alpacaDrip as ad
import datetime
import dbConnector as db


if __name__ == "__main__":

    #start this strategy at 9:35 AM
    if datetime.datetime.now().time() > datetime.time(9,35):
        # Connect to the database
        connector = db.dbConnector()
        connection = connector.createConnection()

        #create time window (5min intervals)
        now = datetime.datetime.now()
        window = datetime.datetime.now() - datetime.timedelta(minutes=5)
        symbols = connector.get
        workingSet = connector.getBarsByTimeWindow(connection, window, now, symbol)
        strategy = ad.Strategy()
        sma = strategy.simpleMovingAverageAcrossTime(workingSet)

        for x in workingSet[0:4]:
            strategy.hammerTimeTrading(sma, x['symbol'], workingSet)
            if strategy.hammerTimeTrading(sma, x['symbol'], workingSet):
                connector.insertTrade(x['symbol'], x['high'], x['low'], x['OPEN'], x['close'], x['volume'], 0, x['barType'], 'hammerTrade', connection)


