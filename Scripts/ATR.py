from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time

def ATR(ohlcv, n):
    df = ohlcv.copy()

    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)

    df['ATR'] = df['TR'].rolling(n).mean()  # Simple Average
    df['exp ATR'] = df['TR'].ewm(span=n, adjust=False, min_periods=n).mean()
    df.dropna(inplace=True)

    df2 = df.drop(['H-L', 'H-PC', "L-PC"], axis=1)
    return df2
