

import yfinance as yf
import pandas as pd
import math

# pulls bid/ask for a specific option contract
# ticker input in string ('AAPL')
# expiry in yyyy-mm-dd format string ('2021-07-02')
# strike is an int
# call is str, C == call, P == put
"""TODO
FIX TO ALLOW STRIKE PRICE TO BE FLOATS (177.5)
"""
def pullPrice(ticker: str, expiry: str, strike: int, call: str):
    exp = expiry[0:4] + '-' + expiry[4:6] + '-' + expiry[6:8]
    
    """Temporary
    """

    data = yf.Ticker(ticker)
    if call == 'C':
        opt = data.option_chain(exp).calls
    else:
        opt = data.option_chain(exp).puts
    selected = opt[opt['strike']==strike]

    bid = selected['bid'].values[0]
    ask = selected['ask'].values[0]

    result = (bid, ask)
    return result

pullPrice('DIS', '20210702', 172.5, 'P')
