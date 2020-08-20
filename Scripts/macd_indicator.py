from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time

def macd(ohlcv, start_time = datetime.today() - timedelta(100) , end_time=datetime.today()):
    # ohlcv = yf.download(ticker, start_time, end_time)
    df = ohlcv.copy()

    print(start_time, end_time)

    df["MA_Fast"] = df["Adj Close"].ewm(span=12, min_periods=12).mean()
    df["MA_Slow"] = df["Adj Close"].ewm(span=26, min_periods=26).mean()
    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span=9, min_periods=9).mean()
    df.dropna(inplace=True)


    df.iloc[:, [4,8,9]].plot()

    return True




start_date = datetime.today() - timedelta(100)
end_date = datetime.today()


macd("MSFT", start_date, end_date)
