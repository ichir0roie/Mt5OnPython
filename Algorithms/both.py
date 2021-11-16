import Scripts.TraderBase

from Scripts.Commons import *


class Trader(Scripts.TraderBase.TraderBase):

    def __init__(self):
        super(Trader, self).__init__()

        self.lotsBase = 0.01

        self.takeProfit = 0.5
        self.stopLoss = 0.1

        self.waitCount = 0
        self.waitTimes = 5

    def onTick(self):
        self.waitCount += 1
        if self.waitCount >= self.waitTimes:
            self.buy()
            self.sell()
        return

    def calcDir(self):
        dir = 0
        ticks = self.market.history[-100:]
        for i in range(1, len(ticks)):
            dirTemp = (ticks[i] - ticks[i - 1]) * i
            dir += dirTemp
        return dir

    def buy(self):
        self.market.openPosition(orderType=OrderType.buy, volume=0.01, takeProfit=self.takeProfit, stopLoss=self.stopLoss)

    def sell(self):
        self.market.openPosition(orderType=OrderType.sell, volume=0.01, takeProfit=self.takeProfit, stopLoss=self.stopLoss)


if __name__ == '__main__':
    t = Trader()
    t.run()
