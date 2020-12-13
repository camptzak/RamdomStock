import yahoo_fin.stock_info as si

def getQuote(symbol):
    try:
        quoteTable = si.get_stats_valuation(symbol)

    except:
        quoteTable = None

    return quoteTable

print(getQuote("AAPL"))


