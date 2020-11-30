import yahoo_fin.stock_info as si

def getQuote(symbol):
    try:
        quoteTable = si.get_quote_table(symbol)

    except:
        quoteTable = None

    return quoteTable


