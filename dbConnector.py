import pymysql.cursors
import pymysql

class dbConnector:
    def __init__(self):
        print("dbObject created")
    def createConnection(self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                 user='root',
                                 #password='admin',
                                 db='GrandExchange',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        return connection

    def insertBar(self, symbol, high, low, open, close, volume, shareCount, barType, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record

                sql = "INSERT INTO `Stonks` (`symbol`, `high`, `low`, `open`, `close`, `volume`, `shareCount`, `barType`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (symbol, high, low, open, close, volume, shareCount, barType))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        except ConnectionError:
            print("Connection Error")
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
    def insertMention(self, symbol, stockwtiz, subreddit2, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record

                sql = "INSERT INTO `Mentions` (`symbol`, `stockwitz`, `subreddit2`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (symbol, stockwtiz, subreddit2))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        except ConnectionError:
            print("Connection Error")
            return False
        finally:
            return True
    def getBarsByTime(self, connection, timestamp):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `timestamp`=%s"
            cursor.execute(sql, (timestamp))
            result = connection.cursor.fetchall()
        return result
    def getBarsByTimeWindow(self, connection , start, end):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Stonks` WHERE `timestamp`>= %s AND `timestamp <= %s"
            cursor.execute(sql, (start, end))
            result = connection.cursor.fetchall()
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
            connection.cursor.execute(sql, (barType))
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
    def getMentions(self):
        return True