
import pandas as pd
from pandas_datareader import data as pdr
from scipy.stats import ttest_ind
from scipy.stats import levene
from scipy import stats
import warnings
import numpy as np
stock_list = ['KO', 'TSLA', 'SPY'] 

def statistics(data):
    # statistical testing for mean daily return 
    #I shall be using the student's t-test for this. THe assumptions that I shall be making are that the two stocks are independent of each other, have the same variance and the same distribution
    #My null hypothesis or H0 shall be that the mean daily returns for the two stocks are equal. 
    KO_stock  = data['KO']
    TSLA_stock = data['TSLA']
    pct_change_tsla = TSLA_stock.pct_change(1).dropna() #get the percent change for tsla stock 
    pct_change_ko = KO_stock.pct_change(1).dropna() #get the percent change for spy stock 
    ttest_val = ttest_ind(pct_change_ko, pct_change_tsla) #gives the t-value, the p-value
    """ Since the p-value is 0.665 > alpha = 0.05 it means that the null hypothesis cannot be rejected. It implies that there is not enough evidence to reject the null hypothesis."""
    print("p-val for part a", ttest_val[1]) 
    #to test for the volatility of two stocks we would use the levene test which calculate the equality of variances 
    #Null hypothesis: there is no significant difference between the volatilities of two stocks.
    #the p-value in this case is 1.16e-26  which is significantly lower than the alpha value. This means that the null hypothesis is rejected and the alternative hypothesis which means that there is a statistically significant difference between the volatilities of the two stocks

    log_returns_ko = (KO_stock/KO_stock.shift(1)).dropna()
    log_returns_tsla = (TSLA_stock/TSLA_stock.shift(1)).dropna()
    log_returns_ko = np.log(log_returns_ko)
    log_returns_tsla = np.log(log_returns_tsla)
    w_val, p_value = levene(log_returns_ko, log_returns_tsla, center = 'mean')
    print("p-value for part b", p_value)

#the alpha represents the benchmark above or below the stock  has done and is the measure of past performance. In this case the stock for tesla was just below the benchmark falling at -0.0005 or -.05%(not too bad). The beta 
#indicates the volatility. In this case the tesla was almost a 100% more volatile than the market!
def capm(data):
    TSLA_stock = data['TSLA']
    SPY_stock = data['SPY']
    TSLA_pct = (TSLA_stock/TSLA_stock.shift(1)).dropna()
    SPY_pct = (SPY_stock/SPY_stock.shift(1)).dropna()
    TSLA_pct = np.log(TSLA_pct)
    SPY_pct = np.log(SPY_pct)
    beta, alpha = np.polyfit(SPY_pct, TSLA_pct, deg = 1)
    print("beta", beta)
    print("alpha", alpha)

#measures the risk-adjusted return of a financial portfolio. Numerator consists of returns over time divided by the standard deviation. In the case the returns the ratio is 0.93 meaning that returns were not accompanies by a lot of volatiluty
def sharpe_ratio(data):
    rfr = 0.02
    stock_returns = data['KO']
    stock_pct = stock_returns.pct_change()
    std_KO = stock_pct.std() * np.sqrt(252)
    cum_KO = (stock_returns[-1]/ stock_returns[0]) -1
    sharpe_ko = (cum_KO - rfr)/std_KO
    print("Sharpe ratio", sharpe_ko)


#statistical measure of the dispersion of prices given. In the case of coco cola the volatility equals 0.14 or 14 percent which makes it not a very volatile stock. 
def volatility_calculator(data):
    stock_returns = data['KO']
    log_return = np.log(stock_returns/stock_returns.shift(1))
    deviation  = log_return.std()
    stock_volatility = deviation * np.sqrt(252)
    print("Volatility", stock_volatility)
    


#is the measure of risk of loss of investments. It estimates how much a set of investments may lose. I calculated historical value at risk which came out to be -3.17. This indicates that the worst possible loss per day at 95% significance level is -3.17%
def vaR_calculator(data): 
    confidence_val = 0.95
    KO_returns = data['KO']
    percent_change_val = KO_returns.pct_change().dropna()
    var_val = np.percentile(percent_change_val, 1- confidence_val) * 100
    print("Var val:", var_val)

#focuses on calculating the risk for returns that fall below the minimum threshold. In this case the MAR or minimum acceptable return is 0 and the downside_dev value was 10.7% which is higher than the MAR return meaning the annual perf was higher than MAT
def downside_dev_calculator(data):
    KO_returns = data['KO'] 
    percent_change_val = KO_returns.pct_change().dropna()
    percent_change_val = percent_change_val[percent_change_val< 0]
    downside_dev = percent_change_val.std() * np.sqrt(252)
    print("downside dev", downside_dev)

#Like downside deviation maximum drawdown is also an indicator of downside risk over time. It is basically the maximum observed loss between the peak and the trough. In this case the drawdown is 8% which means that the losses were relatively small
def max_drawdown(data):
    KO_returns = data['KO']
    percent_change_val = KO_returns.pct_change().dropna()
    cumulative_returns = (1 + percent_change_val).cumprod()
    peak = cumulative_returns.expanding(min_periods = 1).max()
    drawdown = (cumulative_returns/peak) -1 
    print("drawdown", drawdown.min())

def metrics(data):
    volatility_calculator(data)
    vaR_calculator(data)
    downside_dev_calculator(data)
    sharpe_ratio(data)
    max_drawdown(data)

#The ticker is the stock_list which is fed into data_reader for the whole year of 2021. 
data = pdr.get_data_yahoo(stock_list, start = '2021-1-1', end = '2021-12-31')['Adj Close']
######################Part1##############################################################
statistics(data)
metrics(data)
capm(data)



