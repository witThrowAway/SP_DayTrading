import stocktwitScraper
import marketwatchScraper
from redditScraper import scrape
import polygon


#Stocktwits takes last 30 user submitted messages and returns whether bullish or bearish is higher (use as final check)
#print (stocktwitScraper.overallSentiment('IVR'))


'''
#Stocktwits trending stocks that updates every 5 minutes (usually too expensive to correlate)
t = (stocktwitScraper.get_trending_stocks())
print (t)
'''

'''
#Gets all the stocks from MarketWatch screener with specified paramters from original URL ($5 limit)
m_table = (marketwatchScraper.parsePage())
m_stocks = []
for x in m_table:
    m_stocks.append(x.symbol)
'''

'''
#Scrape reddit for most popular stocks in given timeframe in days
r_table = (scrape(2))
r_stocks = []
for x in r_table:
    r_stocks.append(x[0])
'''



'''
#Pull data using Polygon and graph
test_stocks = ('XSPA' ,'MVIS', 'TSLA', 'F', 'AAL', 'LUV', 'APPL')
for stock in test_stocks:
    test_df = polygon.get_stock_history(stock, from_date='2020-06-04', to_date = '2020-06-08')
    print (test_df)

#add patterns
#list_of_patterns = ['CDLMATHOLD', 'CDLSHOOTINGSTAR']
#for pattern in list_of_patterns:
#    test_df[pattern] = polygon.add_pattern(test_df, pattern)
#print(test_df)
'''

#polygon.graphStock(test_stock, test_df, list_of_patterns)





#See what stocks marketwatch and reddit have in common + sentiment analysis
'''
for g in m_stocks:
    if g in r_stocks:
        print(g)
        print (stocktwitScraper.overallSentiment(g))
'''












