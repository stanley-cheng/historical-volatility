''' Script used to calculate the historical volatility of cryptocurrencies present on Yahoo Finance'''

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt

def find_hist_vol(prices, period=30):
    '''
    Calculates and plots the historical volatility given list of prices and the period to calculate historical volatility for different cryptocurrencies using data from Yahoo Finance. Calculated by taking the log of returns using the closing prices on Yahoo Finance.
    
    Parameters
    ----------
    prices: 1d array
        Sorted array of prices from latest to oldest
    period: int
        Period in days for which volatility is calculated for

    Returns
    ----------
    hist_vol: 1d array
        Array of historical volatility calculated from latest price to oldest (size of len(prices) - period)
    '''

    log_returns = np.log(prices[:-1] / prices[1:]) # natural log of returns
    
    hist_vol = np.array([])
    for i in range(len(prices) - period):
        hist_vol = np.append(hist_vol, np.sqrt(365) * np.std(log_returns[i:i+period], ddof=1))

    return hist_vol

# Inputs (user enter inputs here)
period = [10, 30]
currencies = ['ETH-USD', 'BTC-USD', 'MATIC-USD']

# Plot graphs
plt.figure(figsize=(8, 6))
plt.xlabel('Dates')
plt.ylabel('Realized Volatility')

for currency in currencies:
    df = web.DataReader(currency, 'yahoo')
    df = df.sort_values(by=['Date'], ascending=False)

    # Convert dates to date time format
    dates = df.index
    close_prices = df['Close'].to_numpy()

    for i in period:
        plt.plot(dates[:-i], find_hist_vol(close_prices, i), label=f'{currency} {i} Days')

plt.grid()
plt.legend()
plt.show()
