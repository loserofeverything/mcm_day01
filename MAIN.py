from winreg import EnumValue
from customer import customer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from MA import *
from scipy.interpolate import PchipInterpolator as PCHIP
import sympy as sp
import PARAM
from RANDOM import RANDOM
import csv





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








#用于画图
money = np.empty((bitcoin_size,))
dqy_bitcoin = np.empty((bitcoin_size,))
dqy_gold = np.empty((bitcoin_size,))
total_wealth = np.empty((bitcoin_size,))
gold_date_index = 0
mean_wave_bitcoin1 = np.empty((bitcoin_size,))
mean_wave_gold1 = np.empty((gold_size,))
mean_wave_bitcoin2 = np.empty((bitcoin_size,))
mean_wave_gold2 = np.empty((gold_size,))
X_bitcoin = np.linspace(0, bitcoin_size - 1, bitcoin_size)
X_gold = np.linspace(0, gold_size-1, gold_size)



#插值补齐金价
Xtmp = []
Ytmp = []
buy_days = np.zeros((bitcoin_size,))
buy_days_gold = np.zeros((gold_size,))
for i in range(gold_size):
    if not pd.isnull(gold[i]):
        Xtmp.append(i)
        Ytmp.append(gold[i])
pchip = PCHIP(Xtmp, Ytmp)
gold_append = pchip.__call__(X_gold)
dataframe = pd.DataFrame({'Date' : gold_time, 'USD (PM)' : gold_append})
dataframe.to_csv('gold_append.csv', sep=',', index = False)

#赋类中常量
customer.bitcoin_market = bitcoin
customer.bitcoin_premium = PARAM.BITCOIN_PRE
customer.gold_market = gold_append
customer.gold_premium = PARAM.GOLD_PRE

# ##实例化
# dqy = customer(PARAM.USER_MONEY)

# # #用单线法遍历1826天中的每一天
# for date in range(bitcoin_size):
#     #单线法
#     S_MA(dqy, bitcoin, time_sort, gold_append, PARAM.MEANTIME, date, buy_days, buy_days_gold)
    
#     #用来跟踪变量的变化情况来画图
#     money[date] = dqy.money
#     dqy_bitcoin[date] = dqy.bitcoin_amount
#     #统计总资产价值
#     if date in time_sort:
#         gold_date_index = int(np.argmax(time_sort == date))
#         total_wealth[date] = dqy.money + dqy.bitcoin_amount * bitcoin[date] + dqy.gold_amount * gold[gold_date_index]
#     else:
#         total_wealth[date] = dqy.money + dqy.bitcoin_amount * bitcoin[date]


# bit_coin_buy_index = [index for index in np.where(buy_days > 0)[0]]
# bit_coin_sell_index = [index for index in np.where(buy_days < 0)[0]]
# gold_buy_index = [index for index in np.where(buy_days_gold > 0)[0]]
# gold_sell_index = [index for index in np.where(buy_days_gold < 0)[0]]
# print(max(gold_buy_index))

# plt.title("bit coin buy & sell")
# plt.scatter(bit_coin_buy_index, [bitcoin[i] for i in bit_coin_buy_index], c = 'r')
# plt.scatter(bit_coin_sell_index, [bitcoin[i] for i in bit_coin_sell_index], c = 'y')
# plt.plot(X_bitcoin, bitcoin)
# plt.show()


# plt.title("gold buy & sell")
# plt.scatter(gold_buy_index, [gold_append[i] for i in gold_buy_index], c = 'r')
# plt.scatter(gold_sell_index, [gold_append[i] for i in gold_sell_index], c = 'y')
# plt.plot(X_gold, gold_append)
# plt.show()



# #重置
# buy_days = np.zeros((bitcoin_size,))
# buy_days_gold = np.zeros((gold_size,))
# dqy2 = customer(PARAM.USER_MONEY)

# ##使用双线法
# B_MA(dqy2, bitcoin, time_sort, gold_append, PARAM.TIME1, PARAM.TIME2, bitcoin_size,money,dqy_bitcoin,dqy_gold, mean_wave_bitcoin1, mean_wave_gold1, mean_wave_bitcoin2, mean_wave_gold2, buy_days, buy_days_gold)

# bit_coin_buy_index = [index for index in np.where(buy_days > 0)[0]]
# bit_coin_sell_index = [index for index in np.where(buy_days < 0)[0]]
# gold_buy_index = [index for index in np.where(buy_days_gold > 0)[0]]
# gold_sell_index = [index for index in np.where(buy_days_gold < 0)[0]]


# plt.title("bit coin buy sell tendency")
# plt.scatter(bit_coin_buy_index, [bitcoin[i] for i in bit_coin_buy_index], c = 'r')
# plt.scatter(bit_coin_sell_index, [bitcoin[i] for i in bit_coin_sell_index], c = 'y')
# plt.plot(X_bitcoin, mean_wave_bitcoin1, '*--')
# plt.plot(X_bitcoin, mean_wave_bitcoin2)
# plt.plot(X_bitcoin, bitcoin)
# plt.show()



# plt.title("gold buy sell tendency")
# plt.scatter(gold_buy_index, [gold_append[i] for i in gold_buy_index], c = 'r')
# plt.scatter(gold_sell_index, [gold_append[i] for i in gold_sell_index], c = 'y')
# plt.plot(X_gold, mean_wave_gold1, '*--')
# plt.plot(X_gold, mean_wave_gold2)
# plt.plot(X_gold, gold_append)
# plt.show()



#使用随机数法
dqy3 = customer(PARAM.USER_MONEY)
RANDOM_DATE = [i for i in range(0, bitcoin_size, PARAM.RANDOM_TIME)]
if not (bitcoin_size - 1 in RANDOM_DATE):
    RANDOM_DATE.append(bitcoin_size - 1)

ran_money = np.empty((len(RANDOM_DATE),))
ran_dqy_bitcoin = np.empty((len(RANDOM_DATE),))
ran_dqy_gold = np.empty((len(RANDOM_DATE),))
ran_total_wealth = np.empty((len(RANDOM_DATE),))

for i, date in enumerate(RANDOM_DATE):
    RANDOM(date, dqy3, bitcoin, gold_append, time_sort)
    ran_money[i] = dqy3.money
    ran_dqy_bitcoin[i] = dqy3.bitcoin_amount
    ran_dqy_gold[i] = dqy3.gold_amount
    if date in time_sort:
        gold_date_index = int(np.argmax(time_sort == date))
        ran_total_wealth[i] = dqy3.money + dqy3.bitcoin_amount * bitcoin[date] + dqy3.gold_amount * gold[gold_date_index]
    else:
        ran_total_wealth[i] = dqy3.money + dqy3.bitcoin_amount * bitcoin[date]
plt.plot(RANDOM_DATE, ran_dqy_bitcoin)
plt.show()
plt.plot(RANDOM_DATE, ran_dqy_gold)
plt.show()
plt.plot(RANDOM_DATE, ran_money)
plt.show()
plt.plot(RANDOM_DATE, ran_total_wealth)
plt.show()

