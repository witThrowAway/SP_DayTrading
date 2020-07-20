import alpaca_trade_api as tradeapi

from flask import Flask, render_template, request, flash, get_flashed_messages

import dbConnector as db
import backtesting




#Global Variables
ALPACA_KEY_ID = 'PK3VZLXGJAE5FPVLWCOU'
ALPACA_SECRET_KEY = r'NtLnmeY6PtUpPXD2kGblhezLg/6f4lHqEcIqrR/3'

SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


app = Flask(__name__)
app.secret_key=SECRET_KEY

positionsOpen = []
cash = 0
api = tradeapi.REST(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    base_url='https://paper-api.alpaca.markets/'
)


def update_api_keys():
    global api
    api = tradeapi.REST(
        key_id='PKVAPQS1G0L00QDLGCZR',
        secret_key=r'y1HeX5CzRaTIWpTcc2kQHu5zL0xJw6dG2BGQ8sk6',
        base_url='https://paper-api.alpaca.markets/'
    )



@app.route('/', methods = ['GET','POST'])
def dashboard():
    if request.method == 'GET':
        global symbol
        connector = db.dbConnector()
        connection = connector.createConnection()

        scrapedStocks = connector.getMentions(connection);
        symbols = []
        for x in scrapedStocks:
            symbols.append(x['symbol'])

        this = datetime.datetime.today()
        time = str(this.year) + "-" + str(this.month) + "-" + str(this.day) + " " + str(datetime.time(9,35))
        day = str(this.year) + "-" + str(this.month) + "-" + str(this.day)
        trades = connector.getTradeRecents(connection, time)
        stonks = connector.getBarsByTime(connection, time)
        results = connector.getResultsByDate(connection, day)
    if request.method == 'POST':
        symbol = request.form.get('symbol')

        df = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from='2020-07-01', to='2020-07-01').df
        df['timestamp'] = df.index
        df = df.reset_index(drop=True)
        print(df)
        return render_template('graph.html', df = df.to_json(), symbol=symbol)

    return render_template('dashboard_copy.html', symbols = symbols, trades = trades, stonks = stonks, results = results)

@app.route("/graph" , methods=['GET','POST'])
def test():
    return render_template('graph.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    global ALPACA_SECRET_KEY, ALPACA_KEY_ID

    if request.method == 'GET':
        return render_template('config.html')
    if request.method == 'POST':
        try:
            ALPACA_KEY_ID = (request.form.get('alpaca_key_id'))
            ALPACA_SECRET_KEY = (request.form.get('alpaca_secret_key'))
            print('Variables successfully set.')
            update_api_keys()
            return render_template('dashboard.html')
        except:
            print('Variables not successfully set.')
            return render_template('config.html')


@app.route('/backtest', methods=['GET', 'POST'])
def backtest():
    if request.method == 'GET':
        return render_template('backtest.html')
    if request.method == 'POST':
        try:


            cash = request.form.get('cash')
            stocks = (request.form.get('stocks')).split(',')
            from_date = request.form.get('from_date')
            to_date = request.form.get('to_date')
            strat = request.form.get('strat')
            alltrades = 'No trades made'



            print('Starting backtest')


            if strat == 'bband_rsi_algo':
                alltrades = backtesting.algoStart(api, stocks, from_date, to_date, cash)
            #if strat == 'hammer':


            return render_template('backtestresults.html', alltrades=alltrades)
        except Exception as e:
            print(str(e))
            return render_template('dashboard.html')




if __name__ == '__main__':
    app.run()