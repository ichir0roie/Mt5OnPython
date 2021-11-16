from Scripts.Commons import *

import math

import random

# import matplotlib as mpl
import matplotlib.pyplot as plt

class MarketDemo:
    def __init__(self):
        self.price = 100.0
        self.energy=0

        self.ticks = 0
        self.history=[]

        self.positions = []
        self.closedPositions=0

    def getAsk(self):
        return self.price + marketDev

    def getBid(self):
        return self.price - marketDev

    def onTick(self):

        self.forward(1)

        newClosedProfit=0
        newPositions=[]
        for position in self.positions:  # type:Position
            if not position.open:
                continue

            profit = self.calcProfit(position)
            if not (-position.stopLoss < profit < position.takeProfit):
                self.closePosition(position)
                newClosedProfit+=profit
                continue

            newPositions.append(position)

        self.positions=newPositions

        return newClosedProfit

    def getNextTick(self)->float:
        newEnergy=float(random.randint(-1000,1000))*0.001*0.01

        return newEnergy


    def forward(self,times:int):
        for time in range(times):
            self.history.append(self.price)
            self.price += self.getNextTick()
            self.ticks += 1

    def printMarket(self):
        print(self.history)
        x=[i for i in range(len(self.history))]
        plt.plot(x,self.history)
        plt.show()

    def testGetTick(self):
        times=100000
        y=[self.getNextTick() for i in range(times)]
        x=[i for i in range(times)]
        plt.plot(x,y)
        plt.show()

    def testMarketTicks(self):
        self.forward(1000000)
        self.printMarket()


    def openPosition(self, orderType, volume, takeProfit, stopLoss):
        position = Position(
            orderType=orderType,
            openTime=self.ticks,
            openPrice=self.price,
            volume=volume,
            takeProfit=takeProfit,
            stopLoss=stopLoss
        )
        self.positions.append(position)
        return

    def closePosition(self, position):
        position.open = False
        position.closeTime = self.ticks
        position.closedProfit = self.calcProfit(position)

        self.closedPositions+=1

    def getProfitClosed(self):
        profit = 0
        for pos in self.positions:  # type:Position
            if not pos.open:
                profit += pos.closedProfit
        return profit

    def getProfitOpening(self):
        profit = 0
        for pos in self.positions:  # type:Position
            if pos.open:
                profit += self.calcProfit(pos)
        return profit

    def calcProfit(self, position):
        if not position.open:
            return
        dist = self.price - position.openPrice
        profit = 0
        if position.orderType == OrderType.buy:
            profit = dist * position.volume*100
        elif position.orderType == OrderType.sell:
            profit = -dist * position.volume*100

        return profit

    def positionsTotal(self):
        count=0
        for pos in self.positions:
            if pos.open:
                count+=1
        return count




class Position:
    def __init__(self, orderType, openTime, openPrice, volume, takeProfit, stopLoss):

        self.orderType = orderType
        self.openTime = openTime
        self.closeTime = None

        if orderType == OrderType.buy:
            self.openPrice = openPrice + marketDev
        elif orderType == OrderType.sell:
            self.openPrice = openPrice - marketDev
        else:
            raise "orderType not buy or sell"

        self.volume = volume
        self.takeProfit = takeProfit
        self.stopLoss = stopLoss

        self.closedProfit = None

        self.open = True

        return

if __name__ == '__main__':
    mkt=MarketDemo()
    mkt.testMarketTicks()
    # mkt.testGetTick()