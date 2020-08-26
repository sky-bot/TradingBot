from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "AMZN"
start_date = datetime.today() - timedelta(1825)
end_date = datetime.today()

ohlcv = yf.download(ticker, start_date, end_date)

def CAGR(ohlcv, calc="yearly"):
    df = ohlcv.copy()
    df['daily_return'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1 + df['daily_return']).cumprod()
    if calc == "weekly":
        n = len(df)/52
    else:
        n = len(df)/252
    cagr = df['cum_return'][-1]**(1/n) - 1

    return cagr

print(CAGR(ohlcv))

