from datetime import datetime, timedelta
import yfinance as yf
from Scripts.CAGR import CAGR
from Scripts.Volatility import volatility

ticker = "AMZN"
start_date = datetime.today() - timedelta(1825)
end_date = datetime.today()

ohlcv = yf.download(ticker, start_date, end_date)

def sharpe(ohlcv, rf):
    df = ohlcv.copy()

    sr = (CAGR(df)-rf)/volatility(df)

    return sr

print(sharpe(ohlcv, 0.065))