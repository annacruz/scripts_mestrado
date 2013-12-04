#!/usr/bin/env python
# −∗− coding: utf−8 −∗−
from collections import deque


class HoltWinters:
    def __init__(self, alpha, beta, gamma, window_size, temporal_serie):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = 2 #Delta is the margin width
        self.window_size = window_size
        self.temporal_serie = temporal_serie

        """
         Initializing temporal lists as deque, so to add and 
         remove itens on any side of the list the complexity 
         is reduced to O(1)
        """
        self.season_temporal = deque()
        self.trend_temporal = deque()
        self.residual_temporal = deque()
        self.deviation_historical = deque()

        self.season_temporal.append(0)
        self.trend_temporal.append(0)
        self.residual_temporal.append(0)
        self.deviation_historical.append(0)

    def calculate_forecast(self):

        self.calculate_season()
        self.calculate_trend()
        self.calculate_residual()

        self.forecast = self.season_temporal[-1] + self.trend_temporal[-1] + self.residual_temporal[-1]
        return self.forecast

    def calculate_season(self):
        """
        C[t] = gamma * (X[t] - L[t]) + (1 - gamma) * C[t-m]
        """
        before_season = 0
        try:
            before_season = self.season_temporal[-self.window_size]
        except IndexError:
            before_season = 0

        first = (self.gamma) * (self.temporal_serie[-1] - self.residual_temporal[-1])
        second = (1 - self.gamma) * before_season

        self.season_temporal.append(first + second)
        return

    def calculate_trend(self):
        """
        B[t] = beta * (L[t] - L[t-1]) + (1 - beta) * B[t-1] 
        """
        first = self.beta * (self.residual_temporal[-1] - self.residual_temporal[-2])
        second = (1 - self.beta) * self.trend_temporal[-1]

        self.trend_temporal.append(first + second)
        return

    def calculate_residual(self):
        """
        A[t] = alpha * (X[t] - C[t-m]) + (1 - alpha) * (alpha[t-1] + b[t-1]) 
        """
        season = 0
        try:
            season = self.season_temporal[-self.window_size]
        except IndexError:
            season = 0

        first = self.temporal_serie[-1] - season
        second = (1 - self.alpha) * (self.residual_temporal[-1] + self.trend_temporal[-1])

        self.residual_temporal.append(first + second)
        return


    def deviation(self):
        """
        D[t] = gamma * (| X[t] - x[t] |)  + (1 - gamma)*D[t-m]
        """

        deviation = 0
        try:
            deviation = deviation_historical[-self.window_size]
        except IndexError:
            deviation = 0
        
        first = self.gamma * abs(self.temporal_serie[-1] - self.forecast)
        second = 1 - self.gamma * deviation
        self.deviation_historical.append(first + second)
        return

    def confident_band(self):
        """
        [x(t) - (delta * deviation(t)), x(t) + (delta * deviation(t))]
        """
        lower_band = self.forecast - (self.delta * self.deviation_historical[-1])
        upper_band = self.forecast + (self.delta * self.deviation_historical[-1])
        return [lower_band, upper_band]
