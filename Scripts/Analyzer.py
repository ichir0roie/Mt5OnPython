

import Scripts.TraderBase


class Analyzer:
    def __init__(self):

        self.resultList=[]

        return


    def setupTrader(self,
                    td:Scripts.TraderBase.TraderBase,
                    times, baseVolume, tp, st):
        # td = Algorithms.randomWork.Trader()
        # td=Algorithms.trendFollow
        td.takeProfit = tp
        td.stopLoss = st
        td.lotsBase = baseVolume

        td.run(times, False)

        return td

    def judgeModel(self,td:Scripts.TraderBase.TraderBase):

        if td.market.balanceNow >= td.market.balanceInit:
            return True

        return False

    def testRun(self,td):
        resultList=[]
        for volumeRange in range(10):
            volume = (volumeRange+1) * 0.01
            for tpRange in range(11):
                tp=tpRange*0.1
                for stRange in range(11):
                    st=stRange*0.1
                    td.__init__()
                    td.market.historyMode=False
                    td=self.setupTrader(td,500, baseVolume=volume, tp=tp, st=st)
                    td.market.closePositionAll()
                    result=[volume,tp,st,td.market.balanceNow,td.market.closedPositions,td.market.positionsTotal()]
                    resultList.append(result)
                    print(result)
        self.resultList=resultList

    # def testAnalyze(self):


if __name__ == '__main__':
    al=Analyzer()
    import Algorithms.both
    al.testRun(Algorithms.both.Trader())