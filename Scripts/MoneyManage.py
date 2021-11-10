from Scripts.MetaTraderAccess import MetaTraderAccess
from Scripts.Constants import *

class MoneyManage:
    def __init__(self):
        self.accountInfo = AccountInfo()  # type:AccountInfo
        self.candles=Candles() # type:Candles
        self.mta=MetaTraderAccess()

        self.mta.login()

        return

    def loadInfoFromMt5(self):
        info = self.mta.getAccountInfo()
        ai = AccountInfo()
        for key in info:
            value = info[key]
            # print('self.{}=None'.format(key))
            setattr(ai, key, value)
        self.accountInfo = ai

    def printInfo(self):
        for key,value in self.accountInfo.__dict__.items():
            print(key,":",value)

    def loadCandles(self):
        self.candles=self.mta.getRates(pair=USDJPY,timeframe=mt5.TIMEFRAME_M1)
        return

    def judge(self):
        ai=self.accountInfo


class Candles:
    def __init__(self):
        return




class AccountInfo:
    def __init__(self):
        self.login = None
        self.trade_mode = None
        self.leverage = None
        self.limit_orders = None
        self.margin_so_mode = None
        self.trade_allowed = None
        self.trade_expert = None
        self.margin_mode = None
        self.currency_digits = None
        self.fifo_close = None
        self.balance = None
        self.credit = None
        self.profit = None
        self.equity = None
        self.margin = None
        self.margin_free = None
        self.margin_level = None
        self.margin_so_call = None
        self.margin_so_so = None
        self.margin_initial = None
        self.margin_maintenance = None
        self.assets = None
        self.liabilities = None
        self.commission_blocked = None
        self.name = None
        self.server = None
        self.currency = None
        self.company = None


if __name__ == '__main__':
    mm = MoneyManage()
    mm.loadInfoFromMt5()
    # mm.printInfo()
    mm.loadCandles()

    mm.mta.shutdown()