'''
Polygon Setup for Alpaca

https://github.com/alpacahq/Momentum-Trading-Example
https://github.com/alpacahq/example-scalping
https://medium.com/automation-generation/making-your-first-trading-algorithm-1522bba2366e

use ta-lib for quick technical analysis

Relative Strength Index (RSI)
The RSI indicator provides signals that tell investors to buy when the security is oversold and to sell when it is overbought.
High RSI (usually above 70) may indicate a stock is overbought, therefore it is a sell signal.
Low RSI (usually below 30) indicates stock is oversold, which means a buy signal.

Stochastic oscillator

Moving Average Convergence Divergence (MACD).
'''

import alpaca_trade_api as tradeapi
import talib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

api = tradeapi.REST(
    key_id = 'AKI81T1TR0P0KOFHGE9K',
    secret_key = r'6BsKrTdP0WdXSARbufPFV7hVjtwoYGDAx/3ZG9VK',
    base_url = 'https://paper-api.alpaca.markets'
)

def get_stock_history(stock, from_date, to_date):
    df = api.polygon.historic_agg_v2(stock, 1, 'minute', _from=from_date, to=to_date).df
    # Calculates a 60 min simple moving average
    #df["SMA_60_MINS"] = talib.SMA(df["close"], 60)
    # Calculates a 90 min simple moving average
    #df["SMA_90_MINS"] = talib.SMA(df["close"], 90)
    # Calculates RSI for past 30 minutes
    #df["RSI_30_MINS"] = talib.RSI(df["close"], 30)
    # Calculates BBands
    #df['upperband'], df['middleband'], df['lowerband'] = talib.BBANDS(df['close'], timeperiod=15, nbdevup=1.5,
    #                                                                  nbdevdn=1.5, matype=2)

    return df

def graphStock(stock, df, list_of_patterns):

    fig = make_subplots(rows=3+len(list_of_patterns), cols=1, shared_xaxes=True, shared_yaxes=True,vertical_spacing=float(.02))

    SMA_30 = {
      "line": {
        "dash": "solid",
        "color": "black",
        "width": 1.3
      },
      "mode": "lines",
      "name": "30 Min SMA",
      "text": "30 Min SMA",
      "type": "scatter",
      "x": df.index,
      "y": df['SMA_60_MINS']
    }

    SMA_90 = {
      "line": {
        "dash": "solid",
        "color": "grey",
        "width": 1.3
      },
      "mode": "lines",
      "name": "60 Min SMA",
      "text": "60 Min SMA",
      "type": "scatter",
      "x": df.index,
      "y": df['SMA_90_MINS']
    }

    RSI_30_MINS = {
      "line": {
        "dash": "solid",
        "color": "grey",
        "width": 1.3
      },
      "mode": "lines",
      "name": "RSI 30 MINS",
      "text": "RSI 30 MINS",
      "type": "scatter",
      "x": df.index,
      "y": df['RSI_30_MINS'],
    }

    B_LOW = {
      "line": {
        "dash": "solid",
        "color": "pink",
        "width": 1.3
      },
      "mode": "lines",
      "name": "B_LOW",
      "text": "B_LOW",
      "type": "scatter",
      "x": df.index,
      "y": df['lowerband']
    }

    B_MID = {
        "line": {
            "dash": "solid",
            "color": "pink",
            "width": 1.3
        },
        "mode": "lines",
        "name": "B_MID",
        "text": "B_MID",
        "type": "scatter",
        "x": df.index,
        "y": df['middleband']
    }

    B_HIGH = {
        "line": {
            "dash": "solid",
            "color": "pink",
            "width": 1.3
        },
        "mode": "lines",
        "name": "B_UPPER",
        "text": "B_UPPER",
        "type": "scatter",
        "x": df.index,
        "y": df['upperband']
    }

    all_trace_patterns = {}

    for pattern in list_of_patterns:
        all_trace_patterns[pattern] = {"line": {"dash": "solid","color": "orange","width": 2},
                                    "mode": "lines",
                                    "name": pattern,
                                    "text": pattern,
                                    "type": "scatter",
                                    "x": df.index,
                                    "y": df[pattern]}

    fig.append_trace(go.Candlestick(
                        x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'],
                        name='Price'),
                        row=1, col=1)
    fig.append_trace(SMA_30, row=1,col=1)
    fig.append_trace(SMA_90, row=1, col=1)
    fig.append_trace(B_HIGH, row=1, col=1)
    fig.append_trace(B_LOW, row=1, col=1)
    fig.append_trace(B_MID, row=1, col=1)
    fig.append_trace(RSI_30_MINS, row=2, col=1)

    patternNumber = 3
    for p in all_trace_patterns.keys():
        fig.append_trace(all_trace_patterns[p], row=patternNumber, col=1)
        patternNumber+=1

    fig.update_layout(
                        xaxis_type='category',
                        title_text=stock,
                        xaxis = dict(
                                title = 'Time',
                                showticklabels=False),
                        hoverlabel=dict(
                                bgcolor="white",
                                font_size=20,
                                font_family="Rockwell"),
                        height = 2000,
                        xaxis_rangeslider_visible = False
    )



    fig.show()

def add_pattern(df, pattern):
    new_df = eval('talib.' + pattern + '(df.open, df.high, df.low, df.close)')
    return new_df




