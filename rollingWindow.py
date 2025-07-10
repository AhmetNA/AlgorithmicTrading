# region imports
from AlgorithmImports import *
# endregion

class DeterminedSkyBlueDogfish(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2022, 1, 1)
        self.set_end_date(2025, 1, 1)
        self.set_cash(100000)
        
        self.spy = self.add_equity("SPY", Resolution.MINUTE).symbol
        
        self.rollingWindow = RollingWindow[TradeBar](2)
        self.consolidate(self.spy, Resolution.DAILY, self.CustomBarHandler)


        self.schedule.on(self.date_rules.every_day(self.spy),
                        self.time_rules.before_market_close(self.spy, 15),
                        self.ExitPositions) 



    def on_data(self, data: Slice):
        if not self.rollingWindow.is_ready:
            return

        if not (self.time.hour == 9 and self.time.minute == 31):
            return

        if data[self.spy].open >= self.rollingWindow[0].close*1.01:
            self.set_holdings(self.spy, -1)
        elif data[self.spy].open <= self.rollingWindow[0].close*0.99:
            self.set_holdings(self.spy, 1)
        

    def CustomBarHandler(self, bar):
        self.rollingWindow.add(bar)

    def ExitPositions(self):
        self.liquidate(self.spy)