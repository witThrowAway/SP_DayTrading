import dbConnector as db
import datetime

if __name__ == "__main__":
    connector = db.dbConnector()
    connection = connector.createConnection()

    cash = connector.getCash(connection, 8)
    cash = cash[0]['cash']
    this = datetime.datetime.today()
    time = str(this.year) + "-" + str(this.month) + "-" + str(this.day)

    if datetime.datetime.now().time() < datetime.time(9,30):
        connector.setStartCash(connection,cash,time)
    if datetime.datetime.now.time() > datetime.time(4,00):
        connector.endCash(connection,cash,time)
        connector.setResultCash()
