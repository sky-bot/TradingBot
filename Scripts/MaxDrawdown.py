from datetime import datetime, timedelta
import yfinance as yf
from Scripts.CAGR import CAGR
from Scripts.Volatility import volatility

ticker = "AMZN"
start_date = datetime.today() - timedelta(1825)
end_date = datetime.today()

ohlcv = yf.download(ticker, start_date, end_date)

def max_dd(ohlcv):
    df = ohlcv.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1 + df['daily_ret']).cumprod()

    df['cum_roll_max'] = df['cum_return'].cummax()
    df['drawdown'] = df['cum_roll_max'] - df['cum_return']
    df['drawdown_pct'] = df['drawdown']/df["cum_roll_max"]

    max_drop_down = df['drawdown_pct'].max()

    return max_drop_down

