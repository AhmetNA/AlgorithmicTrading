# region imports
from AlgorithmImports import *
from datetime import timedelta
# endregion

class DancingSkyBlueChimpanzee(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2023, 1, 1)
        self.set_end_date(2025, 1, 1)
        self.set_cash(100000)
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        
        # SMA
        self._sma = self.sma(self.spy, 30, Resolution.DAILY)

        history_bars = self.history[TradeBar](self.spy, self._sma.warm_up_period, Resolution.DAILY)

        if history_bars:
            for bar in history_bars:
                self._sma.update(bar)

    def on_data(self, data: Slice):
        if not self._sma.is_ready:
            return

        hist =  self.history(self.spy, timedelta(365), Resolution.DAILY)

        low = min(hist['low'])
        high = max(hist['high'])
        
        price = self.securities[self.spy].price

        if price * 1.05 >= high and self._sma.current.value < price:
            if not self.portfolio[self.spy].is_long:
                self.set_holdings(self.spy, 1)

        elif price*0.95 <= low and self._sma.current.value > price:
            if self.portfolio[self.spy].is_short:
                self.set_holdings(self.spy, -1)

        else:
            self.liquidate()

        self.plot("Benchmark", "52w-High", high)
        self.plot("Benchmark", "52w-Low", low)
        self.plot("Benchmark", "SMA", self._sma.Current.Value)