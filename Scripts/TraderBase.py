import time
import tkinter as tk

import Scripts.MarketDemo


class TraderBase:
    def __init__(self):
        self.balanceInit = 1000000.0
        self.balanceNow = self.balanceInit

        self.market = Scripts.MarketDemo.MarketDemo()

        self.oneRunTicks = 100
        self.waitRunStep = 0.1

        with open("Dat/printInfoFormat.txt", mode="r", encoding="utf-8") as f:
            self.printInfoTextFormat = f.read()

        self.runLoop = False

        # self.tkRoot=tk.Tk()
        # self.setupTk()
        return

    def setupTk(self):
        self.tkText = tk.StringVar()
        self.tkText.set("")
        self.label = tk.Label(self.tkRoot, textvariable=self.tkText)
        self.label.pack()

    def updateTkText(self, text):
        self.tkText.set(text)

    def onTick(self):
        return

    def onTickMarket(self):
        newClosedProfit = self.market.onTick()
        if newClosedProfit != 0:
            self.balanceNow += newClosedProfit

    def runOneTick(self):
        self.onTickMarket()
        self.onTick()

    def printInfo(self):
        # balance: {balance}
        # profitTotal: {profitTotal}
        # positionsOpen: {positionsOpen}
        # positionsTotal: {positionsTotal}

        text = self.printInfoTextFormat.format(
            price=self.market.price,
            ticks=self.market.ticks,
            balance=self.balanceNow,
            profitTotal=self.market.getProfitOpening(),
            positionsTotal=self.market.positionsTotal(),
            positionsHistory=self.market.closedPositions
        ) + "\n"
        print(text)
        # self.updateTkText(text)

    def run(self, times: int = 10000000, printMode: bool = True):
        self.runLoop = True

        while self.market.ticks<times:
            for i in range(self.oneRunTicks):
                self.runOneTick()
            if printMode:
                self.printInfo()
                time.sleep(self.waitRunStep)

                if not self.runLoop:
                    break
