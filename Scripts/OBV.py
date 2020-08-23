import numpy as np
from datetime import datetime

def OBV(ohlcv):
    df = ohlcv.copy()

    df['daily_ret'] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_ret']>=0, 1,-1)
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']

    df['obv'] = df['vol_adj'].cumsum()

    return df['obv']
