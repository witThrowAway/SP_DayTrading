import alpaca_trade_api as tradeapi
import ta
import pandas as pd
import time
import datetime
from numpy import float as floaty
from flask import Flask, render_template, request, flash, get_flashed_messages
import dbConnector as db
import backtesting


#Global Variables
ALPACA_KEY_ID = 'PKKJ09PTT163PO3V428W'
ALPACA_SECRET_KEY = r'kp0o8PWbO/XP1saBZRk98UDK2eQcr6Nacai219NR'
SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

app = Flask(__name__)
app.secret_key=SECRET_KEY

positionsOpen = []
cash = 0

api = tradeapi.REST(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    base_url='https://paper-api.alpaca.markets'
)

def update_api_keys():
    global api
    tradeapi.REST(
        key_id=ALPACA_KEY_ID,
        secret_key=ALPACA_SECRET_KEY,
        base_url='https://paper-api.alpaca.markets'
    )



@app.route('/')
def dashboard():
    return render_template('dashboard.html')

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