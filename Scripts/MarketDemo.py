from Scripts.Commons import *

import math

import random

# import matplotlib as mpl
import matplotlib.pyplot as plt

class MarketDemo:
    def __init__(self):
        self.price = 100.0

        self.ticks = 0
        self.history=[]
        self.historyMode=True
        self.historyMaxLen=1000

        self.positions = []
        self.closedPositions=0
        self.positionsHistoryMode=False


        self.balanceInit = 1000000.0
        self.balanceNow = self.balanceInit

        self.volatilityMax=0.1
        self.volatility=0.01

    def setup(self):
        if self.historyMode:
            self.forward(self.historyMaxLen)

    def getAsk(self):
        return self.price + marketDev

    def getBid(self):
        return self.price - marketDev

    def onTick(self):

        self.forward(1)

        newPositions=[]
        for position in self.positions:  # type:Position
            if not position.open:
                continue

            profit = self.calcProfit(position)
            if not (-position.stopLoss < profit < position.takeProfit):
                self.closePosition(position)
                continue

            newPositions.append(position)

        if not self.positionsHistoryMode:
            self.positions=newPositions


    def setNextPrice(self)->float:

        if self.ticks%100:
            self.volatility= float(random.randint(0, 100)) / 100 * self.volatilityMax

        newEnergy=float(random.randint(-1000,1000))*0.001*self.volatility

        self.price+=newEnergy


    def forward(self,times:int):
        for time in range(times):
            if self.historyMode:
                self.history.append(self.price)
                if len(self.history)>self.historyMaxLen:
                    self.history.pop(0)
            self.setNextPrice()
            self.ticks += 1

    def printMarket(self):
        print(self.history)
        x=[i for i in range(len(self.history))]
        plt.plot(x,self.history)
        plt.show()

    def testGetTick(self):
        times=100000
        y=[self.setNextPrice() for i in range(times)]
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

        self.balanceNow+=position.closedProfit
        self.closedPositions+=1

    def closePositionAll(self):
        for pos in self.positions:
            self.closePosition(position=pos)


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
        # if not position.open:
        #     return
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


    def getBalanceHistory(self):
        profit=self.getProfitClosed()
        balance=self.balanceInit+profit
        return balance



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