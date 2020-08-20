from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["BAJFINANCE.NS", "INFY.NS", "AMZN", "MSFT"]
start_date = datetime.today() - timedelta(3650)
end_date = datetime.today()
close_price = pd.DataFrame()
attemp = 0
drop = []

while len(stocks) != 0 and attemp <=2:
    stocks = [j for j in stocks if j not in drop]
    for i in range(len(stocks)):
        try:
            close_price[stocks[i]] = yf.download(stocks[i], start_date, end_date)["Adj Close"]
            drop.append(stocks[i])
        except:
            print(stocks[i], "Failed to fetch data .... .... retrying")
    attemp += 1

close_price.fillna(method="bfill", axis=0, inplace=True)
daily_return = close_price.pct_change()
cp_standarized = (close_price - close_price.mean())/close_price.std()
cp_standarized.plot()
close_price.plot(subplots=True, layout=(2,2), title="Tech Stock Price", grid=True)


