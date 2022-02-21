from scipy.optimize import linprog
import numpy as np



def calTargetFunc(coelist, mode, gold_amount, bitcoin_amount ,bitcoin_pre, gold_pre, change_list, gold, bitcoin):
    if len(coelist) == 2:
        Acoe = coelist[0]
        Bcoe = coelist[1]
        gold_change = change_list[0]
        bitcoin_change = change_list[1]
        term1 = Acoe*(gold_change + gold_amount) + Bcoe*(bitcoin_amount + bitcoin_change)
    else:
        Bcoe = coelist[0]
        bitcoin_change = change_list[0]
        term1 = Bcoe * (bitcoin_amount + bitcoin_change) 
    if mode == 1:
        return term1 - gold_pre * gold_change * gold - bitcoin_pre * bitcoin_change * bitcoin
    elif mode == 2:
        return term1 - gold_pre * gold_change * gold + bitcoin_pre * bitcoin_change * bitcoin
    elif mode == 3:
        return term1 + gold_pre * gold_change * gold - bitcoin_pre * bitcoin_change * bitcoin
    elif mode == 4:
        return term1 + gold_pre * gold_change * gold + bitcoin_pre * bitcoin_change * bitcoin
    elif mode == 5:
        return term1 - bitcoin_pre * bitcoin_change * bitcoin
    elif mode == 6:
        return term1 + bitcoin_pre * bitcoin_change * bitcoin



def cal_coefficient(mode, bitcoin, future_bitcoin, gold, future_gold, bitcoin_pre, gold_pre):
    if mode == 3:
        return -((future_gold - gold) + gold_pre * gold), -((future_bitcoin - bitcoin) - bitcoin_pre * bitcoin)
    elif mode == 4:
        return -((future_gold - gold) + gold_pre * gold), -((future_bitcoin - bitcoin) + bitcoin_pre * bitcoin)
    elif mode == 2:
        return -((future_gold - gold) - gold_pre * gold), -((future_bitcoin - bitcoin) + bitcoin_pre * bitcoin)
    elif mode == 5:
        return -(future_bitcoin - bitcoin - bitcoin_pre * bitcoin)
    elif mode == 6:
        return -(future_bitcoin - bitcoin + bitcoin_pre * bitcoin)
    elif mode == 1:
        return -((future_gold - gold) - gold_pre * gold), -((future_bitcoin - bitcoin) - bitcoin_pre * bitcoin)

def LinprogPerEquation(mode, bitcoin, gold, bitcoin_amount,gold_amount , bitcoin_pre, gold_pre, money, ccoe_list):
    if mode == 1:
        A = [[gold_pre * gold + gold, bitcoin_pre * bitcoin + bitcoin]]
        b = [[money]]
        LB = [0, 0]
        UB = [None] * 2
        bound = tuple(zip(LB, UB))
        #返回最优解
        return linprog(ccoe_list, A, b, None, None, bound).x
    elif mode == 2:
        A = [[gold_pre * gold + gold, bitcoin - bitcoin_pre * bitcoin]]
        b = [[money]]
        LB = [0, -bitcoin_amount]
        UB = [None, 0]
        bound = tuple(zip(LB, UB))
        #返回最优解
        return linprog(ccoe_list, A, b, None, None, bound).x
    elif mode == 3:
        A = [[gold - gold_pre * gold, bitcoin + bitcoin_pre * bitcoin]]
        b = [[money]]
        LB = [-gold_amount, 0]
        UB = [0, None]
        bound = tuple(zip(LB, UB))
        #返回最优解
        return linprog(ccoe_list, A, b, None, None, bound).x
    elif mode == 4:
        A = [[gold - gold_pre * gold, bitcoin - bitcoin_pre * bitcoin]]
        b = [[money]]
        LB = [-gold_amount, -bitcoin_amount]
        UB = [0, 0]
        bound = tuple(zip(LB, UB))
        #返回最优解
        return linprog(ccoe_list, A, b, None, None, bound).x
    elif mode == 5:
        A = [[bitcoin_pre * bitcoin + bitcoin]]
        b = [[money]]
        LB = [0]
        UB = [None]
        bound = tuple(zip(LB, UB))
        return linprog(ccoe_list, A, b, None, None, bound).x
    elif mode == 6:
        A = [[bitcoin - bitcoin_pre * bitcoin ]]
        b = [[money]]
        LB = [-bitcoin_amount]
        UB = [0]
        bound = tuple(zip(LB, UB))
        return linprog(ccoe_list, A, b, None, None, bound).x


def LinProg(dqy, bitcoin, gold, time_sort, total_days, future_bitcoin, future_gold, bitcoin_pre, gold_pre, money_toprint, gold_toprint, bitcoin_toprint):
    for date in range(total_days):
        if date in time_sort and (date + 1) in time_sort:
            gold_date_index = int(np.argmax(time_sort == date))
            coes = [(future_gold[gold_date_index+1] - gold[gold_date_index]), (future_bitcoin[date+1] - bitcoin[date])]
            change = []
            res_list = []
            #获得每种方案的买卖策略
            for mode in range(1, 5):
                Acoe, Bcoe = cal_coefficient(mode, bitcoin[date], future_bitcoin[date + 1], gold[gold_date_index], future_gold[gold_date_index + 1], bitcoin_pre, gold_pre)
                change.append(LinprogPerEquation(mode, bitcoin[date], gold[gold_date_index], dqy.bitcoin_amount, 
                                    dqy.gold_amount, bitcoin_pre, gold_pre, dqy.money, [Acoe, Bcoe]))
            
            #算出每种买卖策略的结果
            for mode, changel in enumerate(change):
                res_list.append(calTargetFunc(coes, mode+1,dqy.gold_amount, dqy.bitcoin_amount ,bitcoin_pre, gold_pre,  changel, gold[gold_date_index], bitcoin[date]))
            
            #得到最优的买卖策略
            best_change = change[np.where(res_list == np.max(res_list))[0][0]]
            #执行策略
            if best_change[1] < 0 :
                dqy.sell_bitcoin(np.abs(best_change[1]), date)
            elif best_change[1] > 0:
                dqy.buy_bitcoin(best_change[1], date)
            if best_change[0] < 0 :
                dqy.sell_gold(np.abs(best_change[0]), gold_date_index)
            elif best_change[0] > 0:
                dqy.buy_gold(best_change[0], gold_date_index)
        
        #如果今明两天不都是黄金交易日
        else:
            coes = [(future_bitcoin[date+1] - bitcoin[date])]
            change = []
            res_list = []
            for mode in range(5,7):
                Bcoe = cal_coefficient(mode, bitcoin[date], future_bitcoin[date + 1], 114, 514, bitcoin_pre, gold_pre)
                change.append(LinprogPerEquation(mode, bitcoin[date], 114, dqy.bitcoin_amount, 
                                    dqy.gold_amount, bitcoin_pre, gold_pre, dqy.money, [Bcoe]))
                
             #算出每种买卖策略的结果
            for mode, changel in enumerate(change):
                res_list.append(calTargetFunc(coes, mode+5, dqy.gold_amount, dqy.bitcoin_amount ,bitcoin_pre, gold_pre,  changel , 114514, bitcoin[date]))
            #得到最优的买卖策略
            best_change = change[np.where(res_list == np.max(res_list))[0][0]]
            if best_change[0] < 0 :
                dqy.sell_bitcoin(np.abs(best_change[0]), date)
            elif best_change[0] > 0:
                dqy.buy_bitcoin(best_change[0], date)
        

        money_toprint[date] = dqy.money
        gold_toprint[date] = dqy.gold_amount
        bitcoin_toprint[date] = dqy.bitcoin_amount    


                            