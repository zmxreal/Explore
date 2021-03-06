
# coding: utf-8

# In[1]:

#get_ipython().magic('matplotlib inline')


# In[2]:

import numpy as np
import pandas as pd
import seaborn
import statsmodels
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
import logger



# In[ ]:

# calculate z-score
# account for transaction fee
def zscore(series):
    return (series - series.mean()) / np.std(series)

def get_signal(z_score):
    if z_score > 1:
        return('buy1')
    if z_score < -1:
        return('buy2')
    if -1 <= z_score <= 1:
        if z_score >= 0:
            return('side1')
        else:
            return('side2')
        
# In[ ]:
def decision(series1, series2, fee1=0.003, fee2=0.003, min_profit=0.1):
    series = series1 - series2
    mu = series.mean()
    sigma = np.std(series)
    cur_series  = series.iloc[series.shape[0]-1]
    cur_series1 = series1.iloc[series1.shape[0]-1]
    cur_series2 = series2.iloc[series2.shape[0]-1]
    mu_mid = (series1.mean() + series2.mean())/2
    z_score = (cur_series-mu) / sigma
    margin1 = abs(mu_mid - cur_series1*(1+fee1)) - min_profit
    margin2 = abs(mu_mid - cur_series2*(1+fee2)) - min_profit
    #debug usage
    dbg_templet = "p1:%f, p2:%f, mu:%f, sigma:%f, z_score:%f, margin1:%f, margin2:%f"
    dbg_tuple = (series1.iloc[series1.shape[0]-1],series2.iloc[series2.shape[0]-1], mu, sigma, z_score, margin1, margin2)
    logger.debug(("decision: " + dbg_templet)%dbg_tuple)
    #log
    if z_score > 1 and margin2 > 0:
        #log
        logger.debug("=================BUY2")
        return "buy2"
    if z_score < -1 and margin1 > 0:
        #log
        logger.debug("=================BUY1")
        return "buy1"

# In[ ]:
def decision_hua(series1, series2, fee1=0.003, fee2=0.003, min_profit=0.1):
    series = series1 - series2
    mu = series.mean()
    sigma = np.std(series)
    cur_series  = series.iloc[series.shape[0]-1]
    cur_series1 = series1.iloc[series1.shape[0]-1]
    cur_series2 = series2.iloc[series2.shape[0]-1]
    z_score = (cur_series-mu) / sigma
    # pair trading可以同时计算买卖总共的收益情况 
    # buy1 margin       
    margin1 = cur_series2 - cur_series2 * fee2 - cur_series1(1+fee1) -min_profit
    # buy2 margin
    margin2 = cur_series1 - cur_series1 * fee1 - cur_series2(1+fee2) -min_profit
    #debug usage
    dbg_templet = "p1:%f, p2:%f, mu:%f, sigma:%f, z_score:%f, margin1:%f, margin2:%f"
    dbg_tuple = (series1.iloc[series1.shape[0]-1],series2.iloc[series2.shape[0]-1], mu, sigma, z_score, margin1, margin2)
    logger.debug(("decision: " + dbg_templet)%dbg_tuple)
    #log
    if z_score > 1 and margin2 > 0:
        #log
        logger.debug("=================BUY2")
        return "buy2"
    if z_score < -1 and margin1 > 0:
        #log
        logger.debug("=================BUY1")
        return "buy1"
    
# In[ ]:
def sell_decision():
    pass

# In[ ]:
def crisis_detection():
    pass

# In[ ]:
## -----------------------------------------------------------
#
# input format:
#
# return format:
#   ((p1_type,p1_amount, p1_price),(p2_type, p2_amount, p2_price))
#   type: 'buy', 'sell', 'buy_market', 'sell_market'
# QA:
#   1 what's the unit of price? 
## -----------------------------------------------------------
def zhangliang(p1_account, p2_account, p1_data, p2_data):   
    #crisis detection
    
    #check p1 and p2 account
    logger.loggerAccount("ok account", p1_account)
    logger.loggerAccount("huobi account", p2_account)
    logger.loggerList("ok data", p1_data)    
    logger.loggerList("huobi data", p2_data)
    #calculate opportinuty
    p1_serias = pd.Series(p1_data)
    p2_serias = pd.Series(p2_data)
    result = decision(p1_serias, p2_serias, 0.002, 0.002, 0.1)
    #check if we have the ability to execute the transaction
    if result is 'buy1':
        if not (p1_account.cny_fr > 0.01 * p1_data[-1] ) :
            logger.warn(("[P1.!!!] Too few cny. Actual: %f, Need: %f")%(p1_account.cny_fr, 0.01*p1_data[-1]))
            result = None
        if not (p2_account.btc_fr > 0.01):
            logger.warn(("[P2.!!!] Too few btc. Actual: %f, Need: 0.01")%(p2_account.btc_fr))
            result = None
    elif result is 'buy2':
        if not (p2_account.cny_fr > 0.01 * p2_data[-1] ) :
            logger.warn(("[P1.!!!] Too few cny. Actual: %f, Need: %f")%(p2_account.cny_fr, 0.01*p2_data[-1]))
            result = None
        if not (p1_account.btc_fr > 0.01):
            logger.warn(("[P2.!!!] Too few btc. Actual: %f, Need: 0.01")%(p1_account.btc_fr))
            result = None
    # return the result
    if result is 'buy1':    #buy platform1, sell platform2
        return (('buy', 0.01, p1_data[-1]), ('sell', 0.01, p2_data[-1]))
    elif result is 'buy2':  #buy platform2, sell platform1
        return (('sell', 0.01, p1_data[-1]), ('buy', 0.01,  p2_data[-1]))
    else:
        return (None, None)

# In[ ]:
## -------------------------------------
## output states: 
##     buy1,buy2,side1,side2
##     sell1,sell2
##     price1, price2
##     abort
## -------------------------------------
def change_positions(new_state):
    if new_state == 'buy1':
        pass
        # send command to buy 1
        # detect feedback
        # if everything is OK, update my_account
        # else, raise EXCEPTION
    if new_state == 'buy2':
        pass
        # send command to buy 2
        # detect feedback
        # if everything is OK, update my_account
        # else, raise EXCEPTION


# In[ ]:

if __name__ == "__main__":
    """This is main"""
    
    np.random.seed(100)
    mu,sigma = 0, 1 # mean and standard deviation
    x = np.random.normal(mu, sigma, 500)
    y = np.random.normal(mu, sigma, 500)
    X = pd.Series(np.cumsum(x)) + 100
    Y = X + y + 30
    # add trend item for X and Y
    for i in range(500):
        X[i] = X[i] - i/10
        Y[i] = Y[i] - i/10
    plt.plot(X); 
    plt.plot(Y);
    plt.xlabel("Time"); plt.ylabel("Price");
    plt.legend(["X", "Y"]);
    plt.show()
    
    plt.plot(Y-X);
    plt.axhline((Y-X).mean(), color="red", linestyle="--");
    plt.xlabel("Time"); plt.ylabel("Price");
    plt.legend(["Y-X", "Mean"]);
    
    #print mean(Y-X)
    print ((Y-X).mean())
            
    a=decision(X,Y)
    print(a)
        
    #print (Y-X)[-1]
    for i in range(1,100):
        X_slice = X.iloc[(i-1)*5:i*5]
        Y_slice = Y.iloc[(i-1)*5:i*5]
        a=decision(X_slice,Y_slice,0.003,0.003,0.001)
        #print (a)  
    print (X)

