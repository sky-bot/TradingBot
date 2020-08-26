from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ticker = "AMZN"
start_date = datetime.today() - timedelta(1825)
end_date = datetime.today()

ohlcv = yf.download(ticker, start_date, end_date)


def volatility(ohlcv):
    df = ohlcv.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()

    vol = df["daily_ret"].std() * np.sqrt(252)

    return vol
