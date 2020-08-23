import numpy as np
from datetime import datetime
import statsmodels.api as sm

def slope(ser, n):
    slopes = [i*0 for i in range(n-1)]

    for i in range(n, len(ser)+1):
        y = ser[i-1, i]
        x = np.array(range(n))

        x_scaled = (x - x.min())/(x.max() - x.min())
        y_scaled = (y - y.min())/(y.max() - y.min())

        x_scaled = sm.add_constants(x_scaled)
        model = sm.OLS(y_scaled, x_scaled)

        results = model.fit()
        slopes.append(results.params[-1])

    slopes_angle = np.rad2deg(np.arctan(np.array(slopes)))

    return np.array(slopes_angle)