# QUANT CONNECT
# region imports
from AlgorithmImports import *
from datetime import timedelta
# endregion

class MeasuredOrangeFish(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2024, 1, 1)
        self.set_end_date(2025 , 1, 1)
        self.set_cash(100000)

        spy = self.add_equity("SPY", Resolution.DAILY)
        spy.set_data_normalization_mode(DataNormalizationMode.RAW)
        self.spy = spy.symbol


        self.set_benchmark("SPY")
        self.set_brokerage_model(BrokerageName.INTERACTIVE_BROKERS_BROKERAGE, AccountType.MARGIN)

        self.entryPrice = 0 
        self.period = timedelta(days = 31)
        self.next_entry_time = self.time


    def on_data(self, data: Slice):
        if not self.spy in data or data[self.spy] is None:
            return

        price = data[self.spy].close

        if not self.portfolio[self.spy].invested:
            if self.next_entry_time <= self.time:
                self.market_order(self.spy, int(self.portfolio.cash / price))
                self.log("buy spy @" + str(price))
                self.entryPrice = price

        elif self.entryPrice >= 1.1*price or self.entryPrice <= 0.9*price:
            self.liquidate(self.spy)
            self.log("spy sell @" + str(price))
            self.next_entry_time = self.time + self.period
