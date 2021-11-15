
import Scripts.MarketDemo

import time

class TraderBase:
    def __init__(self):
        self.balanceInit=1000000.0
        self.balanceNow=self.balanceInit

        self.market=Scripts.MarketDemo.MarketDemo()

        self.oneRunTicks=100
        self.waitRunStep=0.1

        with open("Dat/printInfoFormat.txt", mode="r", encoding="utf-8") as f:
            self.printInfoTextFormat= f.read()

        self.runLoop=False

        return

    def onTick(self):
        return

    def onTickMarket(self):
        newClosedProfit = self.market.onTick()
        if newClosedProfit !=0:
            self.balanceNow += newClosedProfit

    def runOneTick(self):
        self.onTickMarket()
        self.onTick()

    def printInfo(self):
        # balance: {balance}
        # profitTotal: {profitTotal}
        # positionsOpen: {positionsOpen}
        # positionsTotal: {positionsTotal}

        text=self.printInfoTextFormat.format(
            price=self.market.price,
            ticks=self.market.ticks,
            balance=self.balanceNow,
            profitTotal=self.market.getProfitOpening(),
            positionsTotal=self.market.positionsTotal(),
            positionsHistory=len(self.market.positions)
        )+"\n"
        print(text)

    def run(self):
        self.runLoop=True
        while self.runLoop:
            for i in range(self.oneRunTicks):
                self.runOneTick()
            self.printInfo()
            time.sleep(self.waitRunStep)
