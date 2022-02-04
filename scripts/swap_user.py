
class SwapUser:

    def __init__(self, exposure, collateral_perc, fee_perc):
        self.exposure = exposure
        self.collateral = collateral_perc
        self.collateral_value = collateral_perc * exposure
        self.fee = fee_perc * exposure
        self.is_active = True
        self.is_liquidated = False
        self.quantity = 0
        self.entered_on = 0
        self.exited_on = 0
        self.liquidated_on = 0
        self.profit = 0
        self.entry_price = 0
        self.exit_price = 0

    def enter_swap(self, unix, price):
        self.quantity = self.exposure / price
        self.entered_on = unix
        self.entry_price = price
        return self.entered_on

    def close_swap(self, unix, price):
        self.exited_on = unix
        self.exit_price = price
        self.profit = self.quantity * (self.exit_price - self.entry_price)

        if -1 * self.profit >= self.collateral_value:
            self.is_liquidated = True
            self.treasury_profit = self.fee + (self.collateral_value + self.profit)
        else:
            self.treasury_profit = self.fee

