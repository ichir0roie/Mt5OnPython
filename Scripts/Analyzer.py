import Algorithms.randomWork
from Algorithms import *


class Analyzer:
    def __init__(self):
        return


    def setupAlgo(self,baseVolume,tp,st):
        self.algoRw=Algorithms.randomWork.Trader()
        self.algoRw.takeProfit=tp
        self.algoRw.stopLoss=st
        self.algoRw.lotsBase=baseVolume

    def testRun(self,times,baseVoluem,tp,st):
        self.setupAlgo(baseVoluem,tp,st)
        self.algoRw.run(times,False)

    def judgeModel(self):

        if self.algoRw.balanceNow>=self.algoRw.balanceInit:
            return True

        return False


    def testLooper(self):
        for volumeRage in range(1,10,1):
            volume=
