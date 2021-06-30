import yfinance as yf
import pandas as pd


# pulls bid/ask for a specific option contract
# ticker input in string ('AAPL')
# expiry in yyyy-mm-dd format string ('2021-07-02')
# strike is an int
# call is boolean, True/False. if True == call, False == put
def pullPrice(ticker, expiry, strike, call):
    data = yf.Ticker(ticker)
    if call:
        opt = data.option_chain(expiry).calls
    else:
        opt = data.option_chain(expiry).puts
    selected = opt[opt['strike']==strike]
    bid = selected['bid'].values[0]
    ask = selected['ask'].values[0]

    result = (bid, ask)
    return result

pullPrice('AAPL', '2021-07-16', 140, 'C')


