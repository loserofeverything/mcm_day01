import numpy as np

import PARAM


def sell_b_param(amount):
    return amount

def buy_b_param(money, cur_price):
    return money/cur_price

#用来计算参数b
def all_buy_b_param(means_1, means_2, cur_price_1, cur_price_2, cur_money):
    a =  (means_1 - cur_price_1)/means_1
    b =  (means_2 - cur_price_2)/means_2
    return (a/(a+b)) * (cur_money/cur_price_1)


#用来确定购买或卖掉的个数
def expressions(money, a, judge ,means_1, cur_price_1, means_2, cur_price_2, amount ,mode):
    if mode == 0:##两个都买
        return a + judge * all_buy_b_param(means_1, means_2, cur_price_1, cur_price_2, money)
    elif mode == 1:##一买一卖买的情况
        return a + judge * buy_b_param(money, cur_price_1)
    elif mode == 2:#卖的情况
        return a + judge * sell_b_param(amount)

def judge(means, cur_price):
    return PARAM.OFFSET + ((means - cur_price)/means)

def B_MA_judge(date, means_assert_1_now, means_assert_2_now, means_assert_1_before, means_assert_2_before):
    a = means_assert_1_now - means_assert_2_now
    b = means_assert_1_before - means_assert_2_before
    if date >= 1:
        if a != 0:
            if a * b > 0:
                return 0
            else:
                if a > 0:
                    return 1
                else:
                    return -1
        else:
            if b == 0:
                return 0
            else:
                return -(b/np.abs(b))
    else:
        #第一天就hold
        return 0
    




#-------------------------------------------------------------------

def calM_L(date, time, Assert):
    if date <time:
        return np.mean(Assert[0 : date + 1])
    else:
        return np.mean(Assert[date - time + 1 : date + 1])



#----------------------------------------------------------------------

def S_MA(customer, bitcoin, time_sort, gold, time, date, buy_days, buy_days_gold):
    if date in time_sort:
            #找到黄金数据中对应的那一行
            gold_date_index = int(np.argmax(time_sort == date))

            means_bitcoin = calM_L(date, time, bitcoin)
            means_gold = calM_L(gold_date_index, time, gold)

            j1 = judge(means_bitcoin, bitcoin[date])
            j2 = judge(means_gold, gold[gold_date_index])
            mode1 = 2
            mode2 = 2
            if j1 > 0 and j2 > 0:
                mode1 = 0
                mode2 = 0
            else:
                if j1 > 0:
                    mode1 = 1
                if j2 > 0:
                    mode2 = 1
            
            bitcoin_change = expressions(customer.money, 0, j1 ,means_bitcoin, bitcoin[date], means_gold, gold[gold_date_index], customer.bitcoin_amount, mode1)
            gold_change = expressions(customer.money, 0, j2 ,means_gold, gold[gold_date_index], means_bitcoin, bitcoin[date], customer.gold_amount, mode2)
            
            buy_days[date] = bitcoin_change
            buy_days_gold[gold_date_index] = gold_change


            if bitcoin_change < 0:

                if gold_change >= 0:
                    customer.sell_bitcoin(np.abs(bitcoin_change), date)
                    customer.buy_gold(gold_change, gold_date_index)
                if gold_change < 0:
                    customer.sell_gold(np.abs(gold_change), gold_date_index)
                    customer.sell_bitcoin(np.abs(bitcoin_change), date)
            elif bitcoin_change == 0:  
                if gold_change > 0:
                    customer.buy_gold(gold_change, gold_date_index)
                if gold_change <= 0:
                    customer.sell_gold(np.abs(gold_change), gold_date_index)
            elif bitcoin_change > 0:
                if gold_change <= 0:
                    customer.sell_gold(np.abs(gold_change), gold_date_index)
                    customer.buy_bitcoin(bitcoin_change, date)
                if gold_change > 0:
                    #算出要分钱的权重
                    param_weght_bitcoin = (((means_bitcoin - bitcoin[date])/means_bitcoin)/(((means_bitcoin - bitcoin[date])/means_bitcoin) + ((means_gold - gold[gold_date_index])/means_gold)))
                    param_weght_gold = (((means_gold - gold[gold_date_index])/means_gold)/(((means_bitcoin - bitcoin[date])/means_bitcoin) + ((means_gold - gold[gold_date_index])/means_gold)))
                    #将自己手上的钱按权重分开
                    money_split1 = customer.money * param_weght_bitcoin
                    money_split2 = customer.money * param_weght_gold
                    money_after = 0
                    customer.money = money_split1
                    customer.buy_bitcoin(bitcoin_change, date)
                    money_after += customer.money
                    customer.money = money_split2
                    customer.buy_gold(gold_change, gold_date_index)
                    #买完后统计剩下的钱
                    money_after += customer.money
                    customer.money = money_after
   
   
   
    else:
        #如果这天不是黄金的交易日，那么只需要考虑比特币即可
        means_bitcoin = calM_L(date, time, bitcoin)
        bitcoin_change = customer.bitcoin_amount + ((means_bitcoin - bitcoin[date])/means_bitcoin) * (customer.money/bitcoin[date])
        
        buy_days[date] = bitcoin_change
        if bitcoin_change <= 0:
            customer.sell_bitcoin(np.abs(bitcoin_change), date)
        elif bitcoin_change > 0:
            customer.buy_bitcoin(bitcoin_change, date)




def B_MA(customer, bitcoin, time_sort, 
        gold, time1, time2 ,bitcoin_size,  
        money_toprint, bitcoin_toprint, 
        gold_toprint, mean_wave_bitcoin1, 
        mean_wave_gold1, mean_wave_bitcoin2, 
        mean_wave_gold2, buy_days, buy_days_gold):

    equal_point_bitcoin = np.zeros((2,))
    equal_point_gold = np.zeros((2,))
    means_bitcoin_1_before = 0
    means_gold_1_before = 0
    means_bitcoin_2_before = 0
    means_gold_2_before = 0
    means_bitcoin_1_now = 0
    means_bitcoin_2_now = 0
    means_gold_1_now = 0
    means_gold_2_now = 0
    for date in range(bitcoin_size):
        if date in time_sort:
                #找到黄金数据中对应的那一行
            gold_date_index = int(np.argmax(time_sort == date))
            # #如果还未满 time 天

            means_bitcoin_1_now = calM_L(date, time1, bitcoin)
            means_gold_1_now = calM_L(gold_date_index, time1, gold)
            means_bitcoin_2_now = calM_L(date, time2, bitcoin)
            means_gold_2_now = calM_L(gold_date_index, time2, gold)
            mean_wave_gold1[gold_date_index] = means_gold_1_now
            mean_wave_gold2[gold_date_index] = means_gold_2_now
            mean_wave_bitcoin1[date] = means_bitcoin_1_now
            mean_wave_bitcoin2[date] = means_bitcoin_2_now
            #j < 0 为卖出， j > 0 为买入
            j1 = B_MA_judge(date, means_bitcoin_1_now, means_bitcoin_2_now, means_bitcoin_1_before, means_bitcoin_2_before)
            j2 = B_MA_judge(gold_date_index, means_gold_1_now, means_gold_2_now, means_gold_1_before, means_gold_2_before)
            
            buy_days[date] = j1
            buy_days_gold[gold_date_index] = j2

            
            if j1 < 0:

                if j2 > 0:
                    customer.sell_bitcoin(customer.bitcoin_amount, date)
                    customer.buy_gold(PARAM.ALLIN, gold_date_index)
                if j2 < 0:
                    customer.sell_gold(customer.gold_amount, gold_date_index)
                    customer.sell_bitcoin(customer.bitcoin_amount, date)
                else:
                    pass
            elif j1 == 0:  
                if j2 > 0:
                    customer.buy_gold(PARAM.ALLIN, gold_date_index)
                if j2 <= 0:
                    customer.sell_gold(customer.gold_amount, gold_date_index)
            elif j1 > 0:
                    if j2 <= 0:
                        customer.sell_gold(customer.gold_amount, gold_date_index)
                        customer.buy_bitcoin(PARAM.ALLIN, date)
                    if j2 > 0:
                        #算出当前两个均线相等点分别与过去两个均线相等点值的差与天数差的商
                        diff_bitcoin =np.abs ((equal_point_bitcoin[0] - (means_bitcoin_1_now + means_bitcoin_2_now)/2) / equal_point_bitcoin[0])
                        diff_gold =np.abs ((equal_point_gold[0] - (means_gold_1_now + means_gold_2_now)/2) / equal_point_gold[0])
                        #计算权重
                        param_weght_bitcoin = diff_bitcoin/(diff_bitcoin + diff_gold)
                        param_weght_gold = diff_gold/(diff_bitcoin + diff_gold)
                        #将自己手上的钱按权重分开
                        money_split1 = customer.money * param_weght_bitcoin
                        money_split2 = customer.money * param_weght_gold
                        money_after = 0
                        customer.money = money_split1
                        customer.buy_bitcoin(PARAM.ALLIN, date)
                        money_after += customer.money
                        customer.money = money_split2
                        customer.buy_gold(PARAM.ALLIN, gold_date_index)
                        #买完后统计剩下的钱
                        money_after += customer.money
                        customer.money = money_after
            if j2  != 0:
                equal_point_gold[0] = (means_gold_1_now + means_gold_2_now) / 2
                equal_point_gold[1] = gold_date_index
            if j1 != 0:
                equal_point_bitcoin[0] = (means_bitcoin_1_now + means_bitcoin_2_now) / 2
                equal_point_bitcoin[1] = date           
             
    
        else:
            #如果这天不是黄金的交易日，那么只需要考虑比特币即可
            means_bitcoin_1_now = calM_L(date, time1, bitcoin)
            means_bitcoin_2_now = calM_L(date, time2, bitcoin)
            mean_wave_bitcoin1[date] = means_bitcoin_1_now
            mean_wave_bitcoin2[date] = means_bitcoin_2_now
            j1 = B_MA_judge(date, means_bitcoin_1_now, means_bitcoin_2_now, means_bitcoin_1_before, means_bitcoin_2_before)
            buy_days[date] = j1
            if j1 <= 0:
                customer.sell_bitcoin(customer.bitcoin_amount, date)
            elif j1 > 0:
                customer.buy_bitcoin(PARAM.ALLIN, date)

        
            if j1 != 0:
                equal_point_bitcoin[0] = (means_bitcoin_1_now + means_bitcoin_2_now) / 2
                equal_point_bitcoin[1] = date

        means_bitcoin_1_before = means_bitcoin_1_now
        means_gold_1_before = means_gold_1_now
        means_bitcoin_2_before = means_bitcoin_2_now
        means_gold_2_before = means_gold_2_now
        
        
        money_toprint[date] = customer.money
        bitcoin_toprint[date] = customer.bitcoin_amount
        gold_toprint[date] = customer.gold_amount