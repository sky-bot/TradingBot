from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time

def BollingerBands(ohlcv, n):
    df = ohlcv.copy()

    df['MA'] = df['Ajd Close'].rolling(n).mean()
    df['BB_UP'] = df['MA'] + 2*df['Ma'].rolling(n).std()
    df['BB_DN'] = df['MA'] - 2*df['Ma'].rolling(n).std()
    df['BB_RANGE'] =  df['BB_UP'] - df['BB_DN']
    df.dropna(inplace=True)
    return df
