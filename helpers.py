import urllib
import requests

def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        key = "pk_69ca4942b43144d7907dd72acadf4040"
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={key}")
        response.raise_for_status()
    except requests.RequestException:
        print("Whoa! Key Error!")
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        print("error!")
        return None



plunk = lookup("G41")
blemp = plunk["name"]
print(blemp)

# dfs = pd.read_html(f"https://eoddata.com/stockquote/{exchange}/{symbol}.htm", match='Name')
# dfs = pd.read_html(f"https://eoddata.com/stockquote/NASDAQ/MSFT.htm")
# df = dfs[0]
# print(df)