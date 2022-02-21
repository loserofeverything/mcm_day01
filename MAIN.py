from cProfile import label
from re import X
from matplotlib import projections
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
from linprog_test import LinProg
from mpl_toolkits import mplot3d
import matplotlib.dates as mdates



#用来计算黄金交易日所在黄金表单中的行
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
data3 = pd.DataFrame(pd.read_csv('bit_predict.csv'))
data3_values = data3.values
data4 = pd.DataFrame(pd.read_csv('gold_predict.csv'))
data4_values = data4.values
gold = data2_values[:, 1]
gold_size = gold.size
bitcoin = data1_values[:, 1]
bitcoin_size = bitcoin.size

bit_predict = data3_values.reshape(bitcoin_size,)
gold_predict = data4_values.reshape(gold_size,)




# #####
# data_test = pd.DataFrame(pd.read_excel('wabi.xlsx')).values
# bitcoin = data_test[:, 1]
# print(bitcoin)
# ######


gold_time = data2_values[:, 0]
bitcoin_time = data1_values[:, 0]
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
X_bitcoin_date = [datetime.strptime(d, '%m/%d/%y').date() for d in bitcoin_time]
X_gold_date = [datetime.strptime(d, '%m/%d/%y').date() for d in gold_time]




#插值补齐金价
Xtmp = []
Ytmp = []
Xnull = []
buy_days = np.zeros((bitcoin_size,))
buy_days_gold = np.zeros((gold_size,))
for i in range(gold_size):
    if not pd.isnull(gold[i]):
        Xtmp.append(i)
        Ytmp.append(gold[i])
    elif pd.isnull(gold[i]):
        Xnull.append(i)

pchip = PCHIP(Xtmp, Ytmp)

gold_append = pchip.__call__(X_gold)
gold_added = pchip.__call__(Xnull)
Xnulltime = [gold_time[i] for i in Xnull]
data_added = pd.DataFrame({'Date' : Xnulltime, 'USD (PM)' : gold_added})
dataframe = pd.DataFrame({'Date' : gold_time, 'USD (PM)' : gold_append})
dataframe.to_csv('gold_append.csv', sep=',', index = False)
data_added.to_csv('gold_added.csv', sep=',', index = False)



#赋类中常量
customer.bitcoin_market = bitcoin
customer.bitcoin_premium = PARAM.BITCOIN_PRE
customer.gold_market = gold_append
customer.gold_premium = PARAM.GOLD_PRE










#-------------------------模型使用-------------------------------------------------------------------------#





#-----------------------单线法-----------------------------------------------------------------------------#










# time_for_test = np.arange(1, 50, 5)
# offset_for_test = np.linspace(0, 0.10, 10)
# z_axis_for_test = np.zeros((100,))

# for i1, sub_time_for_test in enumerate(time_for_test):
#     for i2, sub_offset_for_test in  enumerate (offset_for_test):
#         dqy = customer(PARAM.USER_MONEY)
#         #用单线法遍历1826天中的每一天
#         for date in range(bitcoin_size):
#             #单线法
#             S_MA(dqy, bitcoin, time_sort, gold_append, sub_time_for_test, date, buy_days, buy_days_gold, sub_offset_for_test)

#             #用来跟踪变量的变化情况来画图
#             money[date] = dqy.money
#             dqy_bitcoin[date] = dqy.bitcoin_amount
#             dqy_gold[date] = dqy.gold_amount
#             #统计总资产价值
#             if date in time_sort:
#                 gold_date_index = int(np.argmax(time_sort == date))
#                 total_wealth[date] = dqy.money + dqy.bitcoin_amount * bitcoin[date] + dqy.gold_amount * gold_append[gold_date_index]
#             else:
#                 total_wealth[date] = dqy.money + dqy.bitcoin_amount * bitcoin[date] + dqy.gold_amount * gold_append[gold_date_index]
#         #测试最优参数    
#         if sub_time_for_test == 6:
#             if sub_offset_for_test == offset_for_test[-1]:
#                 plt.title("Gold - Bitcoin holdings")
                
#                 #设置日期横坐标
#                 plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#                 plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
                
#                 plt.xlabel("Days")
#                 plt.ylabel("amounts")
#                 plt.plot(X_bitcoin_date, dqy_bitcoin)
#                 plt.plot(X_bitcoin_date, dqy_gold)
#                 plt.legend(labels = ["bitcoin amount", "gold amount"], loc = "best")
#                 plt.gcf().autofmt_xdate() #自动旋转日期标记
#                 plt.savefig("单线法/GoldBitcoinHoldings_Single_mean.png")
#                 plt.show()



#                 plt.title("Money Holdings")

#                 #设置日期横坐标
#                 plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#                 plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))

#                 plt.xlabel("Days")
#                 plt.ylabel("amounts")
#                 plt.plot(X_bitcoin_date, money)
#                 plt.legend(labels = ["money"], loc ='best')
#                 plt.gcf().autofmt_xdate() #自动旋转日期标记
#                 plt.savefig("单线法/MoneyHoldings_Single_mean.png")
#                 plt.show()





#                 plt.title("Total Asset")
#                 plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#                 plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
#                 plt.xlabel("Days")
#                 plt.ylabel("values")
#                 plt.plot(X_bitcoin_date, total_wealth)
#                 plt.legend(labels = ["total asset value"], loc ='best')
#                 plt.gcf().autofmt_xdate() #自动旋转日期标记
#                 plt.savefig("单线法/TotalAsset_Single_mean.png")
#                 plt.show()
#         z_axis_for_test[i1 * 10 + i2] = total_wealth[-1]
        
        
# # z_test = z_axis_for_test.reshape(10,10)
# # data_test = pd.DataFrame(z_test)
# # data_test.to_csv("单均线参数表.csv", sep=',', index = False)




# # plt.figure()
# # ax = plt.axes(projection = '3d')
# # X_FOR_TEST , Y_FOR_TEST = np.meshgrid(time_for_test, offset_for_test, indexing='ij')
# # ax.plot_surface(X_FOR_TEST, Y_FOR_TEST, z_axis_for_test.reshape(10, 10), cmap = 'viridis')
# # ax.set_xlabel("TIME")
# # ax.set_ylabel("OFFSET")
# # ax.set_zlabel("final asset")
# # plt.savefig("param_time_offset.png", dpi =500)
# # plt.show()


# # plt.title("Gold - Bitcoin holdings")
# # plt.xlabel("Days")
# # plt.ylabel("amounts")
# # plt.plot(X_bitcoin, dqy_bitcoin)
# # plt.plot(X_bitcoin, dqy_gold)
# # plt.legend(labels = ["bitcoin amount", "gold amount"], loc = "best")
# # plt.savefig("GoldBitcoinHoldings_Single_mean.png")
# # plt.show()

# # plt.title("Money Holdings")
# # plt.xlabel("Days")
# # plt.ylabel("amounts")
# # plt.plot(X_bitcoin, money)
# # plt.legend(labels = ["money"], loc ='best')
# # plt.savefig("MoneyHoldings_Single_mean.png")
# # plt.show()

# # plt.title("Total Asset")
# # plt.xlabel("Days")
# # plt.ylabel("values")
# # plt.plot(X_bitcoin, total_wealth)
# # plt.legend(labels = ["total asset value"], loc ='best')
# # plt.savefig("TotalAsset_Single_mean.png")
# # plt.show()









# #--------------------------双线法-------------------------------------------------------------------------#
# #用来测试参数
# time1_for_test = np.arange(1, 50, 5)
# distance_between_t1t2 = np.arange(5, 30, 5)

# z_axis_for_test = np.zeros((50,))

# for i1, times in enumerate(time1_for_test):
#     for i2, diff in enumerate(distance_between_t1t2):
#         dqy2 = customer(PARAM.USER_MONEY)
#         B_MA(dqy2, bitcoin, time_sort, gold_append, times, times + diff, bitcoin_size,money,dqy_bitcoin,dqy_gold, mean_wave_bitcoin1, mean_wave_gold1, mean_wave_bitcoin2, mean_wave_gold2, buy_days, buy_days_gold)
#         # #统计总资产
#         for date in range(1826):
#             if date in time_sort:
#                 gold_date_index = int(np.argmax(time_sort == date))
#                 total_wealth[date] = money[date] + dqy_bitcoin[date] * bitcoin[date] + dqy_gold[date] * gold_append[gold_date_index]
#             else:
#                 total_wealth[date] = money[date] + dqy_bitcoin[date] * bitcoin[date] + dqy_gold[date] * gold_append[gold_date_index]
#         # #用来绘制最优参数下的结果
#         if times == 31 and diff == 25:
            
#             bit_coin_buy_index = [index for index in np.where(buy_days > 0)[0]]
#             bit_coin_sell_index = [index for index in np.where(buy_days < 0)[0]]
#             gold_buy_index = [index for index in np.where(buy_days_gold > 0)[0]]
#             gold_sell_index = [index for index in np.where(buy_days_gold < 0)[0]]
#             bit_coin_buy_date = [X_bitcoin_date[i] for i in bit_coin_buy_index]
#             bit_coin_sell_date = [X_bitcoin_date[i] for i in bit_coin_sell_index]
#             gold_buy_date = [X_gold_date[i] for i in gold_buy_index]
#             gold_sell_date = [X_gold_date[i] for i in gold_sell_index]



#             #比特币双平均线对比 及 买入卖出
#             plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#             plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
            
#             plt.xlabel('Date')
#             plt.ylabel('Value')
#             plt.plot(X_bitcoin_date, mean_wave_bitcoin1, 'r--')
#             plt.plot(X_bitcoin_date, mean_wave_bitcoin2)
#             plt.scatter(bit_coin_buy_date, bitcoin[bit_coin_buy_index])
#             plt.scatter(bit_coin_sell_date, bitcoin[bit_coin_sell_index])
#             plt.plot(X_bitcoin_date, bitcoin)

#             plt.legend(labels = ['%d days' %times, '%d days' %(times + diff), 'purchase point', 'sale point', 'bitcoin price'], loc = 'best')
            
#             plt.gcf().autofmt_xdate() #自动旋转日期标记
#             plt.savefig('双线法/BitcoinTwoMeanLine_Two_mean.png')
#             plt.show()

#             #黄金双平均线对比 及 买入卖出
#             plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#             plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
            
#             plt.xlabel('Date')
#             plt.ylabel('Value')
#             plt.plot(X_gold_date, mean_wave_gold1, 'r--')
#             plt.plot(X_gold_date, mean_wave_gold2)
#             plt.scatter(gold_buy_date, gold_append[gold_buy_index])
#             plt.scatter(gold_sell_date, gold_append[gold_sell_index])
#             plt.plot(X_gold_date, gold_append)
#             plt.legend(labels = ['%d days' %times, '%d days' %(times + diff), 'purchase point', 'sale point', 'gold price'], loc = 'best')
#             plt.gcf().autofmt_xdate() #自动旋转日期标记
#             plt.savefig('双线法/GoldTwoMeanLine_Two_mean.png')
#             plt.show()






#             plt.title("Gold - Bitcoin holdings")
#             plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#             plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
#             plt.xlabel("Date")
#             plt.ylabel("Amount")
#             plt.plot(X_bitcoin_date, dqy_bitcoin)
#             plt.plot(X_bitcoin_date, dqy_gold)
#             plt.legend(labels = ["bitcoin holdings", "gold holdings"], loc = "best")
#             plt.gcf().autofmt_xdate() #自动旋转日期标记
#             plt.savefig("双线法/GoldBitcoinHoldings_two_mean.png")
#             plt.show()

#             plt.title("Money Holdings")
#             plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#             plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
#             plt.xlabel("Date")
#             plt.ylabel("Amount")
#             plt.plot(X_bitcoin_date, money)
#             plt.legend(labels = ["money"], loc ='best')
#             plt.gcf().autofmt_xdate() #自动旋转日期标记
#             plt.savefig("双线法/MoneyHoldings_two_mean.png")
#             plt.show()


#             plt.title("Total Asset")
#             plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#             plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
#             plt.xlabel("Date")
#             plt.ylabel("Value")
#             plt.plot(X_bitcoin_date, total_wealth)
#             plt.legend(labels = ['asset value'], loc ='best')
#             plt.gcf().autofmt_xdate() #自动旋转日期标记
#             plt.savefig("双线法/TotalAsset_two_mean.png")
#             plt.show()
#         #用来存每次不同参数下的最终结果
#         z_axis_for_test[i1 * 5 + i2] = total_wealth[-1]

# ##用来画参数 与结果的关系图
# # z_test = z_axis_for_test.reshape(10,5)
# # data_test = pd.DataFrame(z_test)
# # data_test.to_csv("双均线参数表.csv", sep=',', index = False)


# # plt.figure()
# # ax = plt.axes(projection = '3d')
# # X_FOR_TEST , Y_FOR_TEST = np.meshgrid(time1_for_test, distance_between_t1t2, indexing='ij')
# # ax.plot_surface(X_FOR_TEST, Y_FOR_TEST, z_axis_for_test.reshape(10, 5), cmap = 'viridis')
# # ax.set_xlabel("TIME1")
# # ax.set_ylabel("TIME2 - TIME1")
# # ax.set_zlabel("final asset")
# # plt.savefig("双均线参数曲线.png", dpi =500)
# # plt.show()


















#--------------------------随机数法-------------------------------------------------------------------------#







# #用来统计参数 与 最终结果的关系
# time_random_day = np.arange(10, 101, 10)

# ran_total_wealth_all_final = np.empty((10,))

# #随机100次，得到每次最终的结果
# for i1, times in enumerate (time_random_day):
#     #每次随机数法
    
#     RANDOM_DATE = [i for i in range(0, bitcoin_size, times)]
    

#     if not (bitcoin_size - 1 in RANDOM_DATE):
#         RANDOM_DATE.append(bitcoin_size - 1)

#     random_date_format = [X_bitcoin_date[i] for i in RANDOM_DATE]
#     ran_total_wealth_final = np.empty((10,))


#     for cnt in range(10):
#         dqy3 = customer(PARAM.USER_MONEY)
#         ran_money = np.empty((len(RANDOM_DATE),))
#         ran_dqy_bitcoin = np.empty((len(RANDOM_DATE),))
#         ran_dqy_gold = np.empty((len(RANDOM_DATE),))
#         ran_total_wealth = np.empty((len(RANDOM_DATE),))
#         for i, date in enumerate(RANDOM_DATE):
#             RANDOM(date, dqy3, bitcoin, gold_append, time_sort)
#             ran_money[i] = dqy3.money
#             ran_dqy_bitcoin[i] = dqy3.bitcoin_amount
#             ran_dqy_gold[i] = dqy3.gold_amount
#             if date in time_sort:
#                 gold_date_index = int(np.argmax(time_sort == date))
#                 ran_total_wealth[i] = dqy3.money + dqy3.bitcoin_amount * bitcoin[date] + dqy3.gold_amount * gold_append[gold_date_index]
#             else:
#                 ran_total_wealth[i] = dqy3.money + dqy3.bitcoin_amount * bitcoin[date] + dqy3.gold_amount * gold_append[gold_date_index]
#         #用来输出最优参数下的随机数基本统计图表
#         if cnt == 9:
#             if times == 70:
#                 plt.title("Gold - Bitcoin holdings")
#                 plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#                 plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
#                 plt.xlabel("Date")
#                 plt.ylabel("Amount")
#                 plt.plot(random_date_format, ran_dqy_bitcoin)
#                 plt.plot(random_date_format, ran_dqy_gold)
#                 plt.legend(labels = ["bitcoin holdings", "gold holdings"], loc = "best")
#                 plt.gcf().autofmt_xdate() #自动旋转日期标记
#                 plt.savefig("随机数法/GoldBitcoinHoldings_Random.png")
#                 plt.show()

#                 plt.title("Money Holdings")
#                 plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#                 plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
#                 plt.xlabel("Date")
#                 plt.ylabel("Value")
#                 plt.plot(random_date_format, ran_money)
#                 plt.legend(labels = ["money"], loc ='best')
#                 plt.gcf().autofmt_xdate() #自动旋转日期标记
#                 plt.savefig("随机数法/MoneyHoldings_Random.png")
#                 plt.show()

#                 plt.title("Total Asset")
#                 plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#                 plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
#                 plt.xlabel("Date")
#                 plt.ylabel("Value")
#                 plt.plot(random_date_format, ran_total_wealth)
#                 plt.legend(labels = ["total asset value"], loc ='best')
#                 plt.gcf().autofmt_xdate() #自动旋转日期标记
#                 plt.savefig("随机数法/TotalAsset_Random.png")
#                 plt.show()
        
#         ran_total_wealth_final[cnt] = ran_total_wealth[-1]
#     ran_total_wealth_all_final[i1] = np.mean(ran_total_wealth_final)

# data_random_tosave = pd.DataFrame({'交易间隔' : time_random_day, '资产平均值' : ran_total_wealth_all_final})
# data_random_tosave.to_csv('交易间隔_资产平均值.csv', sep=',', index = False)

# plt.title("time gap - mean value of asset")
# plt.xlabel("time gap/Days")
# plt.ylabel("mean value asset/$")
# plt.plot(time_random_day, ran_total_wealth_all_final)
# plt.savefig("交易间隔_资产平均值.png", dpi = 500)
# plt.show()









#--------------------------线性规划 + 预测-------------------------------------------------------------------------#




# money_for_lin = np.empty((1826,))
# gold_for_lin = np.empty((1826,))
# bitcoin_for_lin = np.empty((1826,))
# total_wealth_fo_lin = np.empty((1826,))


# dqy4 = customer(PARAM.USER_MONEY)
# LinProg(dqy4,bitcoin, gold_append, time_sort, 1825, bit_predict, gold_predict,dqy4.bitcoin_premium,dqy4.gold_premium, money_for_lin, gold_for_lin, bitcoin_for_lin)

# for i in range(1825):
#     if i in time_sort:
#         gold_date_index = int(np.argmax(time_sort == i))
#         total_wealth_fo_lin[i] = money_for_lin[i] + bitcoin_for_lin[i] * bitcoin[i] + gold_for_lin[i] * gold_append[gold_date_index]
#     else:
#         total_wealth_fo_lin[i] = money_for_lin[i] + bitcoin_for_lin[i] * bitcoin[i] + gold_for_lin[i] * gold_append[gold_date_index]

# money_for_lin[-1] = dqy4.money
# bitcoin_for_lin[-1] = dqy4.bitcoin_amount
# gold_for_lin[-1] = dqy4.gold_amount


# total_wealth_fo_lin[1825] = money_for_lin[-1] + bitcoin_for_lin[-1] * bitcoin[-1] + gold_for_lin[-1] * gold_append[-1]




# plt.title("Linear programming_predict_total assets")
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
# plt.plot(X_bitcoin_date, total_wealth_fo_lin)
# plt.ylabel("Value")
# plt.xlabel("Date")
# plt.legend(labels = ["asset"], loc = 'best')
# plt.gcf().autofmt_xdate() #自动旋转日期标记
# plt.savefig("线性规划&预测/Linear_programming_predict_total_assets.png", dpi = 500)
# plt.show()

# plt.title("Gold - Bitcoin holdings")
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
# plt.plot(X_bitcoin, bitcoin_for_lin)
# plt.plot(X_bitcoin, gold_for_lin)
# plt.legend(labels = ['bitcoin', 'gold'], loc = 'best')
# plt.ylabel("Amount")
# plt.xlabel("Date")
# plt.gcf().autofmt_xdate() #自动旋转日期标记
# plt.savefig("线性规划&预测/GoldBitcoinHoldings_LPP.png", dpi = 500)
# plt.show()

# plt.title("Money holdings")
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 100))
# plt.plot(X_bitcoin_date, money_for_lin)
# plt.legend(labels = ['money'], loc = 'best')
# plt.ylabel("Value")
# plt.xlabel("Date")
# plt.gcf().autofmt_xdate() #自动旋转日期标记
# plt.savefig("线性规划&预测/MoneyHoldings_LPP.png", dpi = 500)
# plt.show()



