import os
import logging as log
import json
import requests

''' v 0.1 by Jason Haury
 Ported to Python 3 and modified by The Grand Exchange Team
 https://github.com/hamx0r/stocktwits
'''

# StockTwits details
os.environ['ST_ACCESS_TOKEN'] = 'af86bf749e7faefa4f4245d0185a5145c67e7e18'
ST_BASE_URL = 'https://api.stocktwits.com/api/2/'
ST_BASE_PARAMS = dict(access_token=os.getenv('ST_ACCESS_TOKEN'))



class Requests():
    """ Uses `requests` library to GET and POST to Stocktwits, and also to convert resonses to JSON
    """
    def get_json(url, params=None):
        """ Uses tries to GET a few times before giving up if a timeout.  returns JSON
        """
        resp = None
        for i in range(4):
            try:
                resp = requests.get(url, params=params, timeout=5)
            except requests.Timeout:
                trimmed_params = {k: v for k, v in list(params.items()) if k not in list(ST_BASE_PARAMS.keys())}
                log.error('GET Timeout to {} w/ {}'.format(url[len(ST_BASE_URL):], trimmed_params))
            if resp is not None:
                break
        if resp is None:
            log.error('GET loop Timeout')
            return None
        else:
            return json.loads(resp.content)

    def post_json(url, params=None, deadline=30):
        """ Tries to post a couple times in a loop before giving up if a timeout.
        """
        resp = None
        for i in range(4):
            try:
                resp = requests.post(url, params=params, timeout=5)
            except requests.Timeout:
                trimmed_params = {k: v for k, v in list(params.items()) if k not in list(ST_BASE_PARAMS.keys())}
                log.error('POST Timeout to {} w/ {}'.format(url[len(ST_BASE_URL):], trimmed_params))
            if resp is not None:
                break
        return json.loads(resp.content)

R = Requests

def get_stock_stream(symbol, params={}):
    """ gets stream of messages for given symbol
    """
    all_params = ST_BASE_PARAMS.copy()
    for k, v in list(params.items()):
        all_params[k] = v
    return R.get_json(ST_BASE_URL + 'streams/symbol/{}.json'.format(symbol), params=all_params)


def get_message_stream(wl_id, params={}):
    """ Gets up to 30 messages from Watchlist (wl_id) according to additional params
    """
    all_params = ST_BASE_PARAMS.copy()
    for k, v in list(params.items()):
        all_params[k] = v
    return R.get_json(ST_BASE_URL + 'streams/watchlist/{}.json'.format(wl_id), params=all_params)



def get_trending_stocks():
    """ returns list of trending stock symbols, ensuring each symbol is part of a NYSE or NASDAQ
    """
    trending = R.get_json(ST_BASE_URL + 'trending/symbols/equities.json', params=ST_BASE_PARAMS)['symbols']
    symbols = [s['symbol'] for s in trending]
    return symbols



def overallSentiment(stock):

    x = (get_stock_stream(stock))
    num = 0
    bearCount = 0
    bullCount = 0

    for message in x['messages']:
        try:
            basic = (x['messages'][num]['entities']['sentiment']['basic'])
            if (basic == 'Bullish'):
                bullCount += 1
            else:
                bearCount += 1
        except:
            pass
        num += 1

    if bullCount > bearCount:
        return ('Bullish')
    else:
        return ('Bearish')
