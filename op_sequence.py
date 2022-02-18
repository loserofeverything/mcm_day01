from customer import customer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sympy as sp

#用来计算参数b
def b_param(means_1, means_2, cur_price_1, cur_price_2, cur_money):
    a =  (means_1 - cur_price_1)/means_1
    b =  (means_2 - cur_price_2)/means_2
    return (a/(a+b)) * (cur_money/cur_price_1)


#用来确定购买或卖掉的个数
def expressions(cur_money, amount_bitcoin,  amount_gold, means_bitcoin, cur_price_bitcoin, means_gold, cur_price_gold, mode):
    if mode == 0:
        return amount_bitcoin + ((means_bitcoin - cur_price_bitcoin)/means_bitcoin) * b_param(means_bitcoin, means_gold, cur_price_bitcoin, cur_price_gold, cur_money)
    else:
        return amount_gold + ((means_gold - cur_price_gold)/means_gold) * b_param(means_gold, means_bitcoin, cur_price_gold, cur_price_bitcoin, cur_money)

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
X = np.linspace(1, bitcoin_size, bitcoin_size)


#遍历1826天中的每一天
for date in range(bitcoin_size):
    #如果这一天是黄金的交易日
    if date in time_sort:
        #找到黄金数据中对应的那一行
        gold_date_index = int(np.argmax(time_sort == date))
        #如果还未满十天
        if date < 10:
            #则计算从开始投资到当前为止的平均值
            means_bitcoin = np.mean(bitcoin[0 : date + 1])
            means_gold = np.mean(gold[0 : gold_date_index + 1])
        else:
            #如果已满十天则计算十天内的平均值
            means_bitcoin = np.mean(bitcoin[date - 9 : date + 1])
            #且如果黄金交易日数量也满十天
            if gold_date_index >= 10:
                means_gold = np.mean(gold[gold_date_index -9: gold_date_index + 1])
        bitcoin_change = expressions(dqy.money, dqy.bitcoin_amount, dqy.gold_amount, means_bitcoin, bitcoin[date], means_gold, gold[gold_date_index], 0)
        gold_change = expressions(dqy.money, dqy.bitcoin_amount, dqy.gold_amount, means_bitcoin, bitcoin[date], means_gold, gold[gold_date_index], 1)
        #如果要抛售比特币，都是先卖再买
        if bitcoin_change < 0:

            if gold_change >= 0:
                dqy.sell_bitcoin(np.abs(bitcoin_change), date)
                dqy.buy_gold(gold_change, gold_date_index)
            if gold_change < 0:
                dqy.sell_gold(np.abs(gold_change), gold_date_index)
                dqy.sell_bitcoin(np.abs(bitcoin_change), date)
        elif bitcoin_change == 0:  
            if gold_change > 0:
                dqy.buy_gold(gold_change, gold_date_index)
            if gold_change <= 0:
                dqy.sell_gold(np.abs(gold_change), gold_date_index)
        elif bitcoin_change > 0:
            if gold_change <= 0:
                dqy.sell_gold(np.abs(gold_change), gold_date_index)
                dqy.buy_bitcoin(bitcoin_change, date)
            if gold_change > 0:
                #算出要分钱的权重
                param_weght_bitcoin = (((means_bitcoin - bitcoin[date])/means_bitcoin)/((means_bitcoin - bitcoin[date])/means_bitcoin) + ((means_gold - gold[gold_date_index])/means_gold))
                param_weght_gold = (((means_gold - gold[gold_date_index])/means_gold)/((means_bitcoin - bitcoin[date])/means_bitcoin) + ((means_gold - gold[gold_date_index])/means_gold))
                #将自己手上的钱按权重分开
                money_split1 = dqy.money * param_weght_bitcoin
                money_split2 = dqy.money * param_weght_gold
                money_after = 0
                dqy.money = money_split1
                dqy.buy_bitcoin(bitcoin_change, date)
                money_after += dqy.money
                dqy.money = money_split2
                dqy.buy_gold(gold_change, gold_date_index)
                #买完后统计剩下的钱
                money_after += dqy.money
                dqy.money = money_after
    else:
        #如果这天不是黄金的交易日，那么只需要考虑比特币即可
        if date < 10:
            means_bitcoin = np.mean(bitcoin[0 : date + 1])
        else:
            means_bitcoin = np.mean(bitcoin[date - 9 : date + 1])
        bitcoin_change = dqy.bitcoin_amount + ((means_bitcoin - bitcoin[date])/means_bitcoin) * (dqy.money/bitcoin[date])
        if bitcoin_change <= 0:
            dqy.sell_bitcoin(np.abs(bitcoin_change), date)
        elif bitcoin_change > 0:
            dqy.buy_bitcoin(bitcoin_change, date)

    money[date] = dqy.money
    dqy_bitcoin[date] = dqy.bitcoin_amount
    dqy_gold[date] = dqy.gold_amount
    #统计总资产价值
    total_wealth[date] = dqy.money + dqy.bitcoin_amount * bitcoin[date] + dqy.gold_amount * gold[gold_date_index]



plt.plot(X, money)
plt.plot(X,dqy_bitcoin)
plt.plot(X, dqy_gold)
plt.plot(X, total_wealth)
# ax =plt.gca()
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
# ax.spines['bottom'].set_position(('data', np.min(dqy_bitcoin)))
plt.legend(labels = ['dqy money %.2f -- %.2f' %(np.min(money), np.max(money)), 'dqy bitcoin %.2f -- %.2f' %(np.min(dqy_bitcoin) ,np.max(dqy_bitcoin)), 'dqy gold %.2f -- %.2f' %(np.min(dqy_gold), np.max(dqy_gold)), 'dqy total %.2f -- %.2f' %(np.min(total_wealth), np.max(total_wealth))], loc = 'best')
plt.show()

