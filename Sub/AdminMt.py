from datetime import datetime

import MetaTrader5 as mt5
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

import Dat.Account as Account


class AdminMt:
    def __init__(self):
        self.terminalSetup()
        self.lotBase = 0.01
        self.deviationPermitted = 20

    def terminalSetup(self):
        #  connect to MetaTrader 5
        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            mt5.shutdown()
            quit()

        # request connection status and parameters
        print(mt5.terminal_info())
        # get data on MetaTrader 5 version
        print(mt5.version())
        # display data on the MetaTrader 5 package

        print("MetaTrader5 package author: ", mt5.__author__)
        print("MetaTrader5 package version: ", mt5.__version__)

        # display data on MetaTrader 5 version
        print(mt5.version())

    def login(self):
        # connect to the trade account without specifying a password and a server
        # the terminal database password is applied if connection data is set to be remembered
        account = Account.demo
        authorized = mt5.login(
            login=account.login,
            password=account.password,
            server=account.server,
            timeout=10
        )
        if not authorized:
            print("failed to connect at account #{}, error code: {}".format(account.login, mt5.last_error()))
            raise

    def printAccountInfo(self):
        # display trading account data 'as is'
        print(mt5.account_info())
        # display trading account data in the form of a list
        print("Show account_info()._asdict():")
        account_info_dict = mt5.account_info()._asdict()
        for prop in account_info_dict:
            print("  {}={}".format(prop, account_info_dict[prop]))

    def orderOpen(self, symbol="USDJPY", orderType=mt5.ORDER_TYPE_BUY, stopLoss=None, takeProfit=None) -> bool:

        if not self.orderSetup(symbol):
            return False

        lot = self.lotBase

        if orderType == mt5.ORDER_TYPE_BUY:
            price = mt5.symbol_info_tick(symbol).ask
        elif orderType == mt5.ORDER_TYPE_SELL:
            price = mt5.symbol_info_tick(symbol).bid
        else:
            print("not supported.")
            return False

        point = mt5.symbol_info(symbol).point
        deviation = self.deviationPermitted
        request = {}
        request["action"] = mt5.TRADE_ACTION_DEAL
        request["symbol"] = symbol
        request["volume"] = lot
        request["type"] = orderType
        request["price"] = price
        request["deviation"] = deviation
        request["magic"] = 234000
        request["comment"] = "python script open"
        request["type_time"] = mt5.ORDER_TIME_GTC

        if stopLoss is not None:
            request["sl"] = price - float(stopLoss) * point
        if takeProfit is not None:
            request["tp"] = price + float(takeProfit) * point,

        # send a trading request
        result = mt5.order_send(request)
        # check the execution result
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation));
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
            return False

        print("2. order_send done, ", result)
        print("   opened position with POSITION_TICKET={}".format(result.order))

        return True

    def orderClose(self, position: mt5.TradePosition = None) -> bool:

        if not self.orderSetup():
            return False

        self.orderSetup()
        # create a close request

        if position.type == mt5.ORDER_TYPE_BUY:
            price = mt5.symbol_info_tick(position.symbol).bid
            ordertype=mt5.ORDER_TYPE_SELL
        elif position.type == mt5.ORDER_TYPE_SELL:
            price = mt5.symbol_info_tick(position.symbol).ask
            ordertype=mt5.ORDER_TYPE_BUY
        else:
            print("can't setup close. ")
            return False

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": ordertype,
            "position": position.ticket,
            "price": price,
            "magic":position.magic,
            "deviation": self.deviationPermitted,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
        }
        # send a trading request
        result = mt5.order_send(request)
        # check the execution result
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("order_send failed, retcode={}".format(result.retcode))
            print("result", result)
            return False

        print("order close done, ", result)
        print("closed position ={}".format(result.order))

        return True

    def orderSetup(self, symbol=None):

        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            return False

        if symbol is None:
            return True

        # prepare the buy request structure
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            return False

        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", symbol)
                return False
        return True

    def orderGet(self):
        orders = mt5.orders_get()

        if orders is None:
            print("No orders , error code={}".format(mt5.last_error()))
        elif len(orders):
            print("not have orders.")

        return orders

    def positionGet(self):
        positions = mt5.positions_get()
        if positions is None:
            print("No positions , error code={}".format(mt5.last_error()))
            return None
        elif len(positions)==0:
            print("not have positions.")

        return positions

    def positionCloseAll(self):

        positions = self.positionGet()

        ret = True

        for position in positions:  # type:mt5.TradePosition
            success = self.positionClose(position)
            if not success:
                print("error {}".format(position))
                ret = False

        return ret

    def positionClose(self, position: mt5.TradePosition) -> bool:
        if position is None:
            return False

        success = self.orderClose(position)

        return success

    def getTicks(self, pair: str):
        nowTime = datetime.utcnow()
        ticks = mt5.copy_ticks_from(pair, nowTime, 100, mt5.COPY_TICKS_ALL)
        return ticks

    def getRates(self, pair, timeframe):
        # range sample =mt5.TIMEFRAME_H4
        nowTime = datetime.utcnow()
        rates = mt5.copy_rates_from(pair, timeframe, nowTime, 100)
        return rates

    def shutdown(self):
        mt5.shutdown()


if __name__ == '__main__':
    am = AdminMt()
    am.login()

    # rate = am.getRates("USDJPY", mt5.TIMEFRAME_H1)
    # print(rate)

    # am.orderOpen()

    # poss = am.positionGet()
    # for i in poss:
    #     print(i)

    am.positionCloseAll()

    am.shutdown()