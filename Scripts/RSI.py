import numpy as np
from datetime import datetime

def RSI(ohlcv, n):
    df = ohlcv.copy()

    df['delta'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['delta']>=0, df['delta'], 0)
    df['loss'] = np.where(df['delta']<0, abs(df['delta']), 0)

    avg_gain = list()
    avg_loss = list()

    gain = df['gain'].tolist()
    loss = df['loss'].tolist()

    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NAN)
            avg_loss.append(np.NAN)
        elif i==n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        else:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)

    df['avg_gain'] = np.array(avg_gain)
    df['avg_loss'] = np.array(avg_loss)

    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))

    return df