from Scripts.Commons import *


import random

class MarketDemo:
    def __init__(self):
        self.price = 100.0
        self.ticks = 0

        self.positions = []
        self.closedPositions=0

    def getAsk(self):
        return self.price + marketDev

    def getBid(self):
        return self.price - marketDev

    def onTick(self):

        change=float(random.randint(-1000,1000))/1000*0.05
        self.price+=change
        self.ticks+=1

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
