import Algorithms.randomWork


class Analyzer:
    def __init__(self):
        return

    def setupAlgo(self, baseVolume, tp, st):
        self.algoRw = Algorithms.randomWork.Trader()
        self.algoRw.takeProfit = tp
        self.algoRw.stopLoss = st
        self.algoRw.lotsBase = baseVolume

    def testRun(self, times, baseVoluem, tp, st):
        self.setupAlgo(baseVoluem, tp, st)
        self.algoRw.run(times, False)

    def judgeModel(self):

        if self.algoRw.balanceNow >= self.algoRw.balanceInit:
            return True

        return False

    def testLooper(self):
        resultList=[]
        for volumeRange in range(1, 10, 1):
            volume = volumeRange * 0.01
            for tp in range(50,1000,50):
                for st in range(50,1000,50):
                    self.testRun(20000,baseVoluem=volume,tp=tp,st=st)
                    result=[volume,tp,st,self.algoRw.balanceNow]
                    resultList.append(result)
                    print(result)

if __name__ == '__main__':
    al=Analyzer()
    al.testLooper()