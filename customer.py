import numpy as np

class customer(object):

    bitcoin_market = np.empty((1826, ))
    gold_market = np.empty((1265,))
    bitcoin_premium = 0
    gold_premium = 0

    def __init__(self, money):
        self.money = money
        self.bitcoin_amount = 0
        self.gold_amount = 0



    def do_something(self, date, mode):
        if mode == 'bitcoin':
            cost = customer.bitcoin_market[date]
            amount = self.money/((1 + customer.bitcoin_premium)*cost) 
        else:
            cost = customer.gold_market[date]
            amount = self.money/((1 + customer.gold_premium)*cost) 
        return amount 
    
    def buy_bitcoin(self, amount, date):
        new_amount = amount
        if self.money < amount * customer.bitcoin_market[date]:
            new_amount = self.do_something(date, 'bitcoin')
        self.money -= (new_amount * customer.bitcoin_market[date])*(1+customer.bitcoin_premium)
        self.bitcoin_amount += new_amount
     
    def buy_gold(self, amount, date):
        new_amount = amount
        if self.money < amount * customer.gold_market[date]:
            new_amount = self.do_something(date, 'gold')
        self.money -= (new_amount * customer.gold_market[date])*(1+customer.gold_premium)
        self.gold_amount += new_amount

    def sell_bitcoin(self, amount, date):
        new_amount = amount
        if self.bitcoin_amount < amount:
            new_amount = self.bitcoin_amount            
        else:
            self.money += (new_amount *customer.bitcoin_market[date]) *(1 - customer.bitcoin_premium)
            self.bitcoin_amount -= new_amount
    
    def sell_gold(self, amount, date):
        new_amount = amount
        if self.gold_amount < amount:
            new_amount = self.bitcoin_amount
        else:
            self.money += (new_amount *customer.gold_market[date])*(1 - customer.gold_premium)
            self.gold_amount -= new_amount