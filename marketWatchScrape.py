import requests
from bs4 import BeautifulSoup


class marketWatchStock:
    def __init__(self, stock):
        self.symbol = stock[0]
        self.companyName = stock[1]
        self.price = stock[2]
        self.change = stock[3]
        self.changePercent = stock[4]
        self.volume = stock[5]
        self.moreInfo = stock[6]


endpoint = 'https://www.marketwatch.com/tools/stockresearch/screener/results.asp?submit=Screen&Symbol=true&Symbol=false&ChangePct=true&ChangePct=false&FiftyTwoWeekLow=false&CompanyName=true&CompanyName=false&Volume=true&Volume=false&PERatio=false&Price=true&Price=false&LastTradeTime=false&MarketCap=false&Change=true&Change=false&FiftyTwoWeekHigh=false&MoreInfo=true&MoreInfo=false&SortyBy=Price&SortDirection=Descending&ResultsPerPage=OneHundred&TradesShareEnable=true&TradesShareMin=&TradesShareMax=5&PriceDirEnable=true&PriceDir=Up&PriceDirPct=6&LastYearEnable=false&LastYearAboveHigh=&TradeVolEnable=true&TradeVolMin=250000&TradeVolMax=10000000&BlockEnable=false&BlockAmt=&BlockTime=&PERatioEnable=false&PERatioMin=&PERatioMax=&MktCapEnable=false&MktCapMin=&MktCapMax=&MovAvgEnable=false&MovAvgType=Outperform&MovAvgTime=FiftyDay&MktIdxEnable=false&MktIdxType=Outperform&MktIdxPct=&MktIdxExchange=&Exchange=All&IndustryEnable=false&Industry=Accounting'

page = requests.get(endpoint)

soup = BeautifulSoup(page.content, 'html.parser')

tableHead = soup.find_all("thead")
tableBody = soup.find_all("tbody")

headers = tableHead[0].text
headers = headers.split('\n')
while '' in headers:
    headers.remove('')
print(headers)

stocks = tableBody[0].text
stocks = stocks.split('\n\n')
parsedStocks = []
for x in stocks:

    row = (x.split('\n'))
    if row[0] == '':
        del row[0]
    parsedStocks.append(row)

while [] in parsedStocks:
    parsedStocks.remove([])

stockObjects = []

for m in parsedStocks:
    print(m)
    stockObjects.append(marketWatchStock(m))

for x in stockObjects:
    print(x.symbol)
