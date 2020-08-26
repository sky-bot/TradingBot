
def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    n = len(df) / 12
    CAGR = (df["cum_return"].tolist()[-1]) ** (1 / n) - 1
    return CAGR

