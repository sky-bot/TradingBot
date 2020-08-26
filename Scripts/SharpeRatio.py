
from Scripts.CAGR import CAGR
from Scripts.Volatility import volatility

def sharpe(DF, rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf) / volatility(df)
    return sr

