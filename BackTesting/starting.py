import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt
from Scripts.CAGR import CAGR
from Scripts.Volatility import volatility
from Scripts.SharpeRatio import sharpe
from Scripts.MaxDrawdown import max_dd

# Download historical data (monthly) for DJI constituent stocks
tickers = ["ASIANPAINT.NS", "BAJFINANCE.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BHARTIARTL.NS",
          "HCLTECH.NS", "HDFCBANK.NS", "HDFC.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS",
          "INFY.NS", "ITC.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS",
          "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBIN.NS", "SUNPHARMA.NS", "TATASTEEL.NS", "TCS.NS",
          "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS"]

ohlc_mon = {}  # directory with ohlc value for each stock
start = dt.datetime.today() - dt.timedelta(1825)
end = dt.datetime.today()

# looping over tickers and creating a dataframe with close prices
for ticker in tickers:
    ohlc_mon[ticker] = yf.download(ticker, start, end, interval='1mo')
    ohlc_mon[ticker].dropna(inplace=True, how="all")

tickers = ohlc_mon.keys()  # redefine tickers variable after removing any tickers with corrupted data

################################Backtesting####################################

# calculating monthly return for each stock and consolidating return info by stock in a separate dataframe
ohlc_dict = copy.deepcopy(ohlc_mon)
return_df = pd.DataFrame()
for ticker in tickers:
    print("calculating monthly return for ", ticker)
    ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
    return_df[ticker] = ohlc_dict[ticker]["mon_ret"]


# function to calculate portfolio return iteratively
def pflio(DF, m, x):
    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = DF.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(1, len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i, :].mean())
            bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i, :].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
        print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns=["mon_ret"])
    return monthly_ret_df


# calculating overall strategy's KPIs
temp = pflio(return_df, 6, 3)
print(CAGR(temp))
print(sharpe(temp, 0.05))
print(max_dd(temp))

# calculating KPIs for Index buy and hold strategy over the same period
Sensex = yf.download("^BSESN", dt.date.today() - dt.timedelta(1825), dt.date.today(), interval='1mo')
Sensex["mon_ret"] = Sensex["Adj Close"].pct_change()
print(CAGR(Sensex))
print(sharpe(Sensex, 0.05))
print(max_dd(Sensex))

# visualization
fig, ax = plt.subplots()
plt.plot((1 + pflio(return_df, 6, 3)).cumprod())
plt.plot((1 + Sensex["mon_ret"][2:].reset_index(drop=True)).cumprod())
plt.title("Index Return vs Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return", "Index Return"])

