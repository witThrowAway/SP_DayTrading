import pymysql.cursors
import pymysql
from datetime import date

class dbConnector:
    def __init__(self):
        print("dbObject created")
    def createConnection(self):
        # Connect to the database
        connection = pymysql.connect(host='73.186.158.111',
                                 user='trade0',
                                 password='Mountain11231!',
                                 db='GrandExchange',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        return connection

    def insertBar(self, symbol, high, low, open, close, volume, shareCount, barType, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                #print(symbol, high, low, open, close, volume, connection)
                sql = "INSERT INTO `Stonks` (`symbol`, `high`, `low`, `open`, `close`, `volume`, `shareCount`, `barType`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (symbol, high, low, open, close, volume, shareCount, barType))
                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return True
    def insertTrade(self, symbol, high, low, open, close, volume, shareCount, barType, tradeType, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record

                sql = "INSERT INTO `Trades` (`symbol`, `high`, `low`, `open`, `close`, `volume`, `shareCount`, `barType`, `tradeType`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (symbol, high, low, open, close, volume, shareCount, barType, tradeType))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        except ConnectionError:
            print("Connection Error")
            return False
        finally:
            return True
    def insertMention(self, symbol, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record

                sql = "INSERT INTO `Mentions` (`symbol`) VALUES (%s)"
                cursor.execute(sql, (symbol))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        except ConnectionError:
            print("Connection Error")
            return False
        finally:
            return True

    def insertMarketWatchObject(self, symbol, price, change, changePercent, volume, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `MarketWatch` (`symbol`, `price`, `priceChange`, `changePercent`, `volume`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (symbol, price, change, changePercent, volume))

                # connection is not autocommit by default. So you must commit to saveyour changes.
                connection.commit()
        except Exception as e:
            print(str(e))
            return False
        finally:
            return True


    def getBarsByTime(self, connection, timestamp):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `timestamp`=%s"
            cursor.execute(sql, (timestamp))
            result = connection.cursor.fetchall()
        return result
    def getBarsByTimeWindow(self, connection, start, end, symbol):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `symbol` = %s AND `timestamp` BETWEEN %s AND %s ORDER BY symbol ASC"
            cursor.execute(sql, (symbol, start, end))
            result = cursor.fetchall()
        return result
    def getBarsBySymbol(self, connection, symbol):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `symbol`=%s"
            cursor.execute(sql, (symbol))
            result = cursor.fetchall()
        return result
    def getBarsByBarType(self, connection, barType):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `barType`=%s"
            cursor.execute(sql, (barType))
            result = cursor.fetchall()
        return result
    def getTradeByTradeType(self, connection, tradeType):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Trade` WHERE `tradeType`=%s"
            cursor.execute(sql, (tradeType))
            result = cursor.fetchall()
        return result
    def getTradeBySymbol(self, connection, symbol):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Trade` WHERE `symbol`=%s"
            cursor.execute(sql, (symbol))
            result = cursor.fetchall()
        return result
    def getMentions(self, connection):
        with connection.cursor() as cursor:
            timestamp = date.today()
            sql = "SELECT symbol FROM `Mentions` WHERE `timestamp` > %s "
            cursor.execute(sql, timestamp)
            result = cursor.fetchall()
        return result

    def getMarketWatchData(self, connection):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `MarketWatch`"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    def purgeMarketWatchDB(self, connection):
        with connection.cursor() as cursor:
            sql = "Delete FROM `MarketWatch`"
            cursor.execute(sql)
        return True
    def purgeMentions(self, connection):
        with connection.cursor() as cursor:
            sql = "Delete FROM `Mentions`"
            cursor.execute(sql)
        return True