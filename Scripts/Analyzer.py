import Algorithms.randomWork
import Scripts.TraderBase


class Analyzer:
    def __init__(self):

        self.resultList=[]

        return


    def testRun(self, times, baseVolume, tp, st):
        td = Algorithms.randomWork.Trader()
        td.takeProfit = tp
        td.stopLoss = st
        td.lotsBase = baseVolume

        td.run(times, False)

        return td

    def judgeModel(self,td:Scripts.TraderBase.TraderBase):

        if td.balanceNow >= td.balanceInit:
            return True

        return False

    def testRun(self):
        resultList=[]
        for volumeRange in range(10):
            volume = (volumeRange+1) * 0.01
            for tpRange in range(11):
                tp=tpRange*0.1
                for stRange in range(11):
                    st=stRange*0.1
                    td=self.testRun(10000, baseVolume=volume, tp=tp, st=st)
                    result=[volume,tp,st,td.balanceNow,td.market.closedPositions,td.market.positionsTotal()]
                    resultList.append(result)
                    print(result)
        self.resultList=resultList

    # def testAnalyze(self):


if __name__ == '__main__':
    al=Analyzer()
    al.testRun()