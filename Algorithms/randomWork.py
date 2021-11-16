import Scripts.TraderBase

from Scripts.Commons import *


import random

class Trader(Scripts.TraderBase.TraderBase):

    def __init__(self):
        super(Trader, self).__init__()

        self.lotsBase=0.01

        self.takeProfit=0.1
        self.stopLoss=0.1

        self.waitCount=0
        self.waitTimes=5


    def onTick(self):
        self.waitCount+=1
        if self.waitCount>=self.waitTimes:
            dir=random.randint(0,1)
            if dir>0:
                self.buy(self.lotsBase,self.takeProfit,self.stopLoss)
            else:
                self.sell(self.lotsBase, self.takeProfit, self.stopLoss)
            self.waitCount=0

        return


    def buy(self,volume,takeProfit,stopLoss):
        self.market.openPosition(orderType=OrderType.buy,volume=volume,takeProfit=takeProfit,stopLoss=stopLoss)

    def sell(self,volume,takeProfit,stopLoss):
        self.market.openPosition(orderType=OrderType.sell,volume=volume,takeProfit=takeProfit,stopLoss=stopLoss)



if __name__ == '__main__':
    t=Trader()
    t.run()