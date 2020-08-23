import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

from Scripts.ATR import ATR


def ADX(ohlcv, n):
    df = ohlcv.copy()
    print(len(df))

    df['TR'] = ATR(df, 14)['TR']
    df['DMplus'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), df['High'] - df['High'].shift(1), 0)
    df['DMplus'] = np.where(df['DMplus'] < 0, 0, df['DMplus'])
    df['DMminus'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)),
                              df['Low'].shift(1) - df['Low'], 0)
    df['DMminus'] = np.where(df['DMminus'] < 0, 0, df['DMminus'])

    TRn = list()
    DMplusN = list()
    DMminusN = list()

    TR = df['TR'].tolist()
    DMplus = df['DMplus'].tolist()
    DMminus = df['DMminus'].tolist()

    for i in range(len(df)):
        if i < n:
            TRn.append(np.NAN)
            DMplusN.append(np.NAN)
            DMminusN.append(np.NAN)
        elif i == n:
            TRn.append(df['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df['DMminus'].rolling(n).sum().tolist()[n])
        else:
            TRn.append(TRn[i-1] - (TRn[i-1]/14) + TR[i])
            DMplusN.append(DMplusN[i-1] - DMplusN[i-1]/14 + DMplus[i])
            DMminusN.append(DMminusN[i-1] - DMminusN[i-1]/14 + DMminus[i])

    df['TRn'] = np.array(TRn)
    df['DMplusN'] = np.array(DMplusN)
    df['DMminusN'] = np.array(DMminusN)
    df['DIplusN'] = 100 * (df['DMplusN'] / df['TRn'])
    df['DIminusN'] = 100 * (df['DMminusN'] / df['TRn'])
    df['DIdiff'] = abs(df['DIplusN'] - df['DIminusN'])
    df['DIsum'] = df['DIplusN'] + df['DIminusN']
    df['DX'] = 100 * (df['DIdiff'] / df['DIsum'])
    ADX = []
    DX = df['DX'].tolist()
    for j in range(len(df)):
        if j < 2 * n - 1:
            ADX.append(np.NaN)
        elif j == 2 * n - 1:
            ADX.append(df['DX'][j - n + 1:j + 1].mean())
        elif j > 2 * n - 1:
            ADX.append(((n - 1) * ADX[j - 1] + DX[j]) / n)
    df['ADX'] = np.array(ADX)
    return df['ADX']


print("Program Started")
ohlcv = yf.download('AAPL', datetime.today() - timedelta(60), datetime.now())
print(ADX(ohlcv, 14))