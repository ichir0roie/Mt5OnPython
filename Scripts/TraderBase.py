import time
import tkinter as tk

import Scripts.MarketDemo


class TraderBase:
    def __init__(self):

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

    def runOneTick(self):
        self.market.onTick()
        self.onTick()

    def printInfo(self):
        # balance: {balance}
        # profitTotal: {profitTotal}
        # positionsOpen: {positionsOpen}
        # positionsTotal: {positionsTotal}

        text = ""

        valueDict = {
            "price": self.market.price,
            "ticks": self.market.ticks,
            "balance": self.market.balanceNow,
            "profitTotal": self.market.getProfitOpening(),
            "positionsTotal": self.market.positionsTotal(),
            "positionsHistory": self.market.closedPositions,
            "winRate": self.checkWinRate()
        }

        for key in valueDict.keys():
            textTemp = key
            while len(textTemp) < 20:
                textTemp += " "
            textTemp +=": " + str(valueDict[key]) + "\n"
            text+=textTemp

        print(text + "\n")
        # self.updateTkText(text)

    def checkWinRate(self):
        sum = 0.0
        win = 0.0
        for pos in self.market.positions:  # type:Scripts.MarketDemo.Position
            if not pos.open:
                if pos.closedProfit > 0:
                    win += 1
                sum += 1
        if win==0:
            return 0
        return  win/sum

    def run(self, times: int = 10000000, printMode: bool = True):
        self.runLoop = True

        self.market.setup()
        self.market.positionsHistoryMode = True

        while self.market.ticks < times:
            for i in range(self.oneRunTicks):
                self.runOneTick()
            if printMode and times % 100 == 0:
                self.printInfo()
                time.sleep(self.waitRunStep)

                if not self.runLoop:
                    break
