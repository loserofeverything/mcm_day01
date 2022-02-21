import numpy as np

def getRandomWeight(mode):
    if mode == 0:
        np.random.seed()
        randlist = np.random.uniform(0.1, 1, (3,))
        sums = np.sum(randlist)
        return [randlist[0]/sums, randlist[1]/sums, randlist[2]/sums]
    else:
        np.random.seed()
        randlist = np.random.uniform(0.1, 1, (2,))
        sums = np.sum(randlist)
        return [randlist[0]/sums, randlist[1]/sums]

def Pump(dqy, mode ,mark, date):
    if mode == 0:
        pass
    elif mode == 1:
        dqy.sell_bitcoin(dqy.bitcoin_amount - mark/dqy.bitcoin_market[date], date)
    elif mode == 2:
        dqy.sell_gold(dqy.gold_amount - mark/dqy.gold_market[date], date)

def Flood(dqy, mode ,mark, date):
    if mode == 0:
        pass
    elif mode == 1:
        dqy.buy_bitcoin(mark/dqy.bitcoin_market[date] - dqy.bitcoin_amount, date)
    elif mode == 2:
        dqy.buy_gold(mark/dqy.gold_market[date] - dqy.gold_amount, date)


def RANDOM(date, dqy, bitcoin, gold, time_sort):
    
    if date in time_sort:
        gold_date_index = int(np.argmax(time_sort == date))
        assetlist = [dqy.money, dqy.bitcoin_amount * bitcoin[date], dqy.gold_amount * gold[gold_date_index]]
        self_asset = np.sum(assetlist)
        Expections = getRandomWeight(0)
        Exp_list = self_asset * np.array([Expections[2],Expections[1],Expections[0] ])
        i = 0
        
        for Exp, actual in zip(Exp_list, assetlist):
            if i!= 2:
                if actual > Exp:
                    Pump(dqy, i, Exp, date)
            else:
                if actual > Exp:
                    Pump(dqy, i, Exp, gold_date_index)
            i += 1
        i = 0
        for Exp, actual in zip(Exp_list, assetlist):
            if i != 2:
                if actual < Exp:
                    Flood(dqy, i, Exp, date)
            else:
                if actual < Exp:
                    Flood(dqy, i, Exp, gold_date_index)
            i += 1
    else:
        assetlist = [dqy.money, dqy.bitcoin_amount * bitcoin[date]]
        self_asset = np.sum(assetlist)
        i = 0
        Expections = getRandomWeight(1)
        Exp_list = self_asset * np.array([Expections[1], Expections[0]])
        for Exp, actual in zip(Exp_list, assetlist):
            if actual > Exp:
                Pump(dqy, i, Exp, date)
            i += 1
        i = 0
        for Exp, actual in zip(Exp_list, assetlist):
            if actual < Exp:
                Flood(dqy, i, Exp, date)
            i += 1
        
                
        
