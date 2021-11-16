import Scripts.TraderBase

from Scripts.Commons import *


class Trader(Scripts.TraderBase.TraderBase):

    def __init__(self):
        super(Trader, self).__init__()

        self.lotsBase = 0.01

        self.takeProfit = 0.2
        self.stopLoss = 0.1

        self.waitCount = 0
        self.waitTimes = 5

    def onTick(self):
        self.waitCount += 1
        if self.waitCount >= self.waitTimes:

            dir = self.calcDir()
            # dir*=-1

            if dir > 0:
                self.buy(self.lotsBase, self.takeProfit, self.stopLoss)
            else:
                self.sell(self.lotsBase, self.takeProfit, self.stopLoss)
            self.waitCount = 0

        return

    def calcDir(self):
        dir = 0
        ticks = self.market.history[-100:]
        for i in range(1, len(ticks)):
            dirTemp = (ticks[i] - ticks[i - 1]) * i
            dir += dirTemp
        return dir

    def buy(self, volume, takeProfit, stopLoss):
        self.market.openPosition(orderType=OrderType.buy, volume=volume, takeProfit=takeProfit, stopLoss=stopLoss)

    def sell(self, volume, takeProfit, stopLoss):
        self.market.openPosition(orderType=OrderType.sell, volume=volume, takeProfit=takeProfit, stopLoss=stopLoss)


if __name__ == '__main__':
    t = Trader()
    t.market.setup()
    t.run()
