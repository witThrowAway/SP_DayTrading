import dbConnector as db
import datetime
#import time
from datetime import time

if __name__ == "__main__":
    connector = db.dbConnector()
    connection = connector.createConnection()

    cash = connector.getCash(connection, 8)
    cash = cash[0]['cash']
    this = datetime.datetime.today()
    time = str(this.year) + "-" + str(this.month) + "-" + str(this.day)

    if datetime.datetime.now().time() < datetime.time(9,30):
        connector.setStartCash(connection,cash,time)
    else:
        connector.setEndCash(connection,cash,time)
        connector.setResultCash(connection)
