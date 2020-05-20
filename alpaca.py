import alpaca_trade_api as tradeapi
import datetime
import autoDD

BASE_URL = 'https://paper-api.alpaca.markets'
KEY_ID = 'PKFSSL2YNYE244YZ7XOI'
SECRET_KEY = 'yDHsNCUjYodpYsWXj4OZSe1ieQO9JltbT0JJBfYL'

api = tradeapi.REST(KEY_ID, SECRET_KEY, BASE_URL)

# Only look for stocks with the following criteria
minimumPrice = .15
maximumPrice = 5.00


def buy(symbol, quantity, buy_price, limit_price, stop_price):
    api.submit_order(symbol=symbol,
                     qty=quantity,
                     side='buy',
                     time_in_force='day',
                     type='limit',
                     limit_price=buyPrice,
                     order_class='bracket',
                     stop_loss=dict(stop_price=stop_price),
                     take_profit=dict(limit_price=limit_price))


# Return boolean to see if the market is open
def is_market_open():
    if not api.get_clock().is_open:
        return False
    else:
        return True


if __name__ == '__main__':
    print('---')
    print (datetime.datetime.now())
    account = api.get_account()
    print('Your cash: $', account.cash)
    print('Your buying power: $', account.buying_power)

    print('Market open?: ' + str(is_market_open()))

    # scrapeWebForStocks() -----> return list of possible stocks and feed into analyze stocks
    scraped_stocks = autoDD.main()
    for stock in scraped_stocks:        #Make sure we have only valid stocks
        try:
            api.get_asset(stock[0])
        except:
            scraped_stocks.remove(stock)


    #try the bracket order
    stock = 'NNDM'
    quotePrice = api.get_last_quote(stock)
    buyPrice = float(quotePrice.askprice)
    limitPrice = buyPrice * 1.02
    stopPrice = buyPrice * .97

    print(api.get_barset(symbols=stock, timeframe='1Min', limit=1000))

    try:
        buy(stock, quantity=50, buy_price=buyPrice, limit_price=limitPrice, stop_price=stopPrice)
        print ('Bought 50 shares of ' + stock)
        print ('\tCost: ', buyPrice)
        print('\tLimit: ', limitPrice)
        print('\tStop: ', stopPrice)
    except Exception as e:
        print ('There was an error buying your stock: ' + str(e))


    # analyzeStocks(list_of_scraped_stocks) --->  takes in list of stocks and analyzes them: using volume, % increase should be between 5% and 10% ish, etc. (ran every XXXX often)


    # runAlgo() ---> threaded execution of algo on analyzed stocks ----> order submissions and constantly running
