from datetime import datetime
from Scripts.ATR import ATR
from stocktrends import Renko



def GetRenko(DF, n):
    df = DF.copy()
    df.reset_index(inplace=True)
    df = df.iloc[:, [0,1,2,3,5,6]]
    df.columns = ["date", "open", "high", "low", "close", "volume"]

    renko_df = Renko(df)
    renko_df.brick_size = round(ATR(DF, 120)['ATR'][-1], 0)

    df2 = renko_df.get_bricks()

    return df2

    pass
