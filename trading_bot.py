#!/usr/bin/env python
# coding: utf-8

# In[523]:


import pandas as pd
ticker=input("enter symbol of stock you want to analyse : ")

df = pd.read_csv("./dataset/CSV/"+ticker+".csv")
df= df.drop(['Low', 'High','Volume','Adjusted Close'], axis=1)
df
df['Stock Ticker']=[ticker]*len(df.index)


# In[524]:


df['50dayEWM'] = df['Open'].ewm(span=50, adjust=False).mean()
df['200dayEWM'] = df['Open'].ewm(span=200, adjust=False).mean()


# In[525]:


def rsi(df, periods = 12, ema = True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df['Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi
df['rsi']=rsi(df)


# In[526]:


df


# In[527]:


import matplotlib.pyplot as plt

plt.plot(df['Open'], label=ticker)
plt.plot(df['50dayEWM'], label='50-day EWM')
plt.plot(df['200dayEWM'], label='200-day EWM')
plt.legend(loc=2)



# In[528]:


previous_50 = df['50dayEWM'].shift(1)
previous_200 = df['200dayEWM'].shift(1)
crossing = (((df['50dayEWM'] <= df['200dayEWM']) & (previous_50 >= previous_200))
            | ((df['50dayEWM'] >= df['200dayEWM']) & (previous_50 <= previous_200)))


# In[529]:


crossing_dates = df.loc[crossing]


# In[530]:


df['Date'] = pd.to_datetime(df['Date'])


# In[531]:


previous_50 = df['50dayEWM'].shift(1)
previous_200 = df['200dayEWM'].shift(1)
buys = (((df['50dayEWM'] <= df['200dayEWM']) & (previous_50 >= previous_200)))


# In[532]:


previous_50 = df['50dayEWM'].shift(1)
previous_200 = df['200dayEWM'].shift(1)
sells = (((df['50dayEWM'] >= df['200dayEWM']) & (previous_50 <= previous_200)))


# In[533]:


buy_dates = df.loc[buys]
sell_dates = df.loc[sells]
buy_dates


# In[534]:


buyindex=df.index[buys].tolist()
buy_dates
profit=0
loss=0
profits=[]
rsi_list=[]
for i in buyindex:
    if i>200 and i<len(df)-300 and df.loc[i]['Open'] !=0:
        buy=df.loc[i]['Open']
        for j in range(i,i+265):
            
            p=df.loc[j]['Open']-buy
            if p/buy<-0.1:                
                loss=loss+1
                profits.append(p/buy)
                rsi_list.append(df.loc[i]['rsi'])
                break
            elif p/buy>0.1:
                profit=profit+1
                profits.append(p/buy)
                rsi_list.append(df.loc[i]['rsi'])
                break
        if j-i==264:
            if buy<df.loc[j]['Open']:
                profit=profit+1
                profits.append((df.loc[j]['Open']-buy)/buy)
                rsi_list.append(df.loc[i]['rsi'])
            else :
                profit.append((df.loc[j]['Open']-buy)/buy)
                rsi_list.append(df.loc[i]['rsi'])
                loss=loss+1


# In[535]:


print(profit,loss)


# In[536]:


fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(rsi_list, profits, color ='maroon',
        width = 0.4)
 
plt.xlabel("rsi")
plt.ylabel("profit")
plt.show()
plt.savefig(ticker+'.png')


# In[537]:


cap=1
for i in profits:
    cap=cap*(1+i)
print("capital invested in ",ticker, " is multiplied by ",cap-1)


# In[ ]:




