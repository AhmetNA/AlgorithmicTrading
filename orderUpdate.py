# QUANT CONNECT
# region imports
from AlgorithmImports import *
# endregion

class FocusedBlackPelican(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2022, 1, 1)
        self.set_end_date(2025, 1, 1)
        self.set_cash(100000)

        self.qqq = self.add_equity("QQQ" , Resolution.DAILY).symbol

        self.entry_ticket = None
        self.stop_market_ticket = None
        self.entry_time = None
        self.stop_market_order_fill_time = None
        self.highest_price = 0 

    def on_data(self, data: Slice):
        if self.stop_market_order_fill_time is not None:
            if(self.time - self.stop_market_order_fill_time).days < 30:
                return

        price = self.securities[self.qqq].price

        if not self.portfolio.invested and not self.transactions.get_open_orders(self.qqq):
            quantity = self.calculate_order_quantity(self.qqq, 0.9)
            self.entry_ticket = self.limit_order(self.qqq, quantity, price, "Entry Ticket")
            self.entry_time = self.time


        if (self.time - self.entry_time).days > 1 and self.entry_ticket.status != OrderStatus.FILLED:
            self.entry_time = self.time
            update_fields = UpdateOrderFields()
            update_fields.limit_price = price
            self.entry_ticket.update(update_fields)

        if self.stop_market_ticket is not None and self.portfolio.invested:
            if self.highest_price < price:
                self.highest_price = price
                update_fields = UpdateOrderFields()
                update_fields.stop_price = price*0.95
                self.stop_market_ticket.update(update_fields)


    def OnOrderEvent(self, orderEvent):
        if orderEvent.status != OrderStatus.FILLED:
            return
        
        if self.entry_ticket is not None and self.entry_ticket.order_id == orderEvent.order_id:
            self.stop_market_ticket = self.stop_market_order(self.qqq, -self.entry_ticket.quantity, 
                                                            0.95*self.entry_ticket.average_fill_price) 
        

        if self.stop_market_ticket is not None and self.stop_market_ticket.order_id == orderEvent.order_id:
            self.stop_market_order_fill_time = self.time
            self.highest_price = 0