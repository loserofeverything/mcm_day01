from cProfile import label
from customer import customer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from MA import *
import sympy as sp





#用来存储黄金的交易日 形如：
#1
#3
#4
#5
#6
#9
#################
def calcuTimeSort(time ,base):
    t1 = [ int(i) for i in base.split('/') ]
    t2 = [ int(i) for i in time.split('/') ]
    d1 = datetime(t1[2], t1[0], t1[1])
    d2 = datetime(t2[2], t2[0], t2[1])
    dif = d2 - d1
    return dif.days


#读入数据
data1 = pd.DataFrame(pd.read_csv('BCHAIN-MKPRU.csv'))
data1_values = data1.values
data2 = pd.DataFrame(pd.read_csv('LBMA-Gold.csv'))
data2_values = data2.values
gold = data2_values[:, 1]
gold_size = gold.size
bitcoin = data1_values[:, 1]
bitcoin_size = bitcoin.size




# #####
# data_test = pd.DataFrame(pd.read_excel('wabi.xlsx')).values
# bitcoin = data_test[:, 1]
# print(bitcoin)
# ######


gold_time = data2_values[:, 0]
base_date = data1_values[0, 0]
time_sort = np.array([calcuTimeSort(time, base_date) for time in gold_time])



#赋类中常量
customer.bitcoin_market = bitcoin
customer.bitcoin_premium = 0.02
customer.gold_market = gold
customer.gold_premium = 0.01

#实例化
dqy = customer(1000)


#用于画图
money = np.empty((bitcoin_size,))
dqy_bitcoin = np.empty((bitcoin_size,))
dqy_gold = np.empty((bitcoin_size, ))
total_wealth = np.empty((bitcoin_size,))
gold_date_index = 0
means_vec = np.empty((bitcoin_size,))
X = np.linspace(1, bitcoin_size, bitcoin_size)
X2 = np.linspace(1, bitcoin_size-1, bitcoin_size-1)
X3 = np.linspace(1, gold_size, gold_size)
BITCOIN_CHANGE = np.empty((bitcoin_size,))

#用单线法遍历1826天中的每一天
# for date in range(bitcoin_size):
#     #单线法
#     S_MA(dqy, bitcoin, time_sort, gold, 5, date)
    
#     #用来跟踪变量的变化情况来画图
#     money[date] = dqy.money
#     dqy_bitcoin[date] = dqy.bitcoin_amount
#     #统计总资产价值
#     total_wealth[date] = dqy.money + dqy.bitcoin_amount * bitcoin[date] + dqy.gold_amount * gold[gold_date_index]

B_MA(dqy, bitcoin, time_sort, gold, 5,10, bitcoin_size,money,dqy_bitcoin,dqy_gold)

plt.plot(X, money)
plt.plot(X, dqy_bitcoin)
plt.show()
print(total_wealth[1825])
print(dqy.bitcoin_amount)
print(money[1825])
#print(dqy.gold_amount)
print("%.32f" %np.min(money))
print("%.32f" %np.min(dqy_bitcoin))