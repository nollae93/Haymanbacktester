import overnight_basket
import config

import time 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime

def make_stategy_result_data(data):
    temp_data = data

    roll_max_strategy = temp_data['Basket'].rolling(len(temp_data.index), min_periods=1).max()
    daily_drawdown_strategy = temp_data['Basket'] / roll_max_strategy - 1.0
    max_daily_drawdown_strategy = daily_drawdown_strategy.rolling(len(temp_data.index), min_periods=1).min()
    max_draw_dowm_strategy = round(abs(pd.Series.min(max_daily_drawdown_strategy)) * 100, 2)

    return_portfolio_log = np.log(temp_data['Basket'] / temp_data['Basket'].shift(1))
    volatility_month = pd.DataFrame.rolling(return_portfolio_log, window = 20).std() * np.sqrt(20)
    volatility_year = pd.DataFrame.rolling(return_portfolio_log, window = 252).std() * np.sqrt(252)

    temp_data.insert(len(temp_data.columns), "daily_drawdown", daily_drawdown_strategy)
    temp_data.insert(len(temp_data.columns), "max_draw_down", max_daily_drawdown_strategy)
    temp_data.insert(len(temp_data.columns), "volatility_month", volatility_month)
    temp_data.insert(len(temp_data.columns), "volatility_year", volatility_year)

    return temp_data

class show_result_strategy():
    def __init__(self, trading_data):
        self.manufactured_data = make_stategy_result_data(trading_data)
        

    def show_strategy_result(self):
        data = self.manufactured_data.drop(len(self.manufactured_data.index) - 1)
        
        start_date = str(data.at[0, 'Date'])
        end_date = str(data.at[len(data.index) - 1, 'Date'])
        
        total_return = data.at[len(data.index) - 1, 'Basket'] / data.at[0, 'Basket'] 
        cagr = round(((total_return)**(1/int(len(data.index)/365.0)) - 1), 4) * 100
        max_draw_down = round(abs(pd.Series.min(data["max_draw_down"])) * 100, 2)
        volatility_average_month = np.nanmean(data["volatility_month"])
        volatility_average_year = np.nanmean(data["volatility_year"])

        print('Strategy : %s' %config.strategy_name)
        print('start : %s-%s-%s' %(start_date[:4], start_date[4:6],start_date[6:8]))
        print('end   : %s-%s-%s' %(end_date[:4], end_date[4:6], end_date[6:8]))
        print('----------------------')
        print('Total Return : %.2f %%' %(total_return * 100))
        print('CAGR  : %.2f %%' %cagr)
        print('MDD   : %.2f %%' %max_draw_down)
        print('Month Volatility : %.4f %%' %volatility_average_month)
        print('Year Volatility : %.4f %%' %volatility_average_year)

    def show_asset_growth_graph(self):
        data = self.manufactured_data
        
        fig = plt.figure(figsize=(16, 9))

        top_axes = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)
        bottom_axes = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)

        top_axes.plot(data.index, data['Basket'], label='Basket')

        bottom_axes.plot(data.index, data["daily_drawdown"], label="daily_drawdown")
        bottom_axes.plot(data.index, data["max_draw_down"], label="max_draw_down")

        top_axes.legend(loc='best')
        data.to_excel("./Backtest_result.xlsx", encoding = 'euc_KR')

        plt.savefig("./graph.png", dpi=240)       
        plt.title('graph')
        plt.tight_layout()
        plt.show()
        plt.close(fig)





