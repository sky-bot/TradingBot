from datetime import datetime, timedelta
import yfinance as yf
from Scripts.CAGR import CAGR
from Scripts.MaxDrawdown import max_dd


ticker = "AMZN"
start_date = datetime.today() - timedelta(1825)
end_date = datetime.today()

ohlcv = yf.download(ticker, start_date, end_date)

def calmar(ohlcv):
    df = ohlcv.copy()

    _calmar = CAGR(df)/max_dd(df)
    return _calmar

print(calmar(ohlcv))
