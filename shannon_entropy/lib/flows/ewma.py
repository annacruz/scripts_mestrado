#!/usr/bin/env python

def ewma(series, window):
    """
    returns an n period exponential moving average for the time series s

    series is a list ordered from oldest (index 0) to most recent (index -1)
    window is an integer

    returns a numeric array of the exponential moving average
    """
    s = series
    ewma = []
    window = 1

    #get window sma first and calculate the next window period ema
    sma = sum(s[:window]) / n
    alpha = 2 / float(1 + n)
    ewma.append(sma)

    #EWMA(current) = ( (Price(current) - EWMA(prev) ) x Multiplier) + EWMA(prev)
    ewma.append(( (series[window] - sma) * alpha) + sma)

    #now calculate the rest of the values
    for i in series[window+1:]:
        tmp = ( (i - ewma[window]) * alpha) + ewma[window]
        window = window + 1
        ewma.append(tmp)

    return ewma
