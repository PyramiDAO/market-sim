
class SwapUser:

    def __init__(self, exposure, collateral_perc, monthly_fee_perc):
        self.exposure = exposure
        self.collateral = collateral_perc
        self.collateral_value = collateral_perc * exposure
        self.monthly_fee = monthly_fee_perc * exposure

        self.entered_on = 0
        self.exited_on = 0

        self.entry_price = 0
        self.exit_price = 0

        self.quantity = 0
        self.profit = 0
        self.total_swap_fee = 0

        self.is_active = True
        self.is_liquidated = False
        self.liquidated_on = 0

        
    def enter_swap(self, unix, price):
        self.quantity = self.exposure / price
        self.entered_on = unix
        self.entry_price = price

    def force_liquidated(self, unix, price):
        self.is_liquidated = True
        
        self.exited_on = unix
        self.exit_price = price
        
        self.profit = self.quantity * (self.exit_price - self.entry_price)

        # calculate how many 30 day period elapsed between user entering and exiting swap
        elapsed_periods = (self.exited_on - self.entered_on) / (30 * 86400) # 86400 seconds in a day
        self.total_swap_fee = elapsed_periods * self.monthly_fee

        self.treasury_profit = self.total_swap_fee + (self.collateral_value + self.profit)

    def close_swap(self, unix, price):
        self.exited_on = unix
        self.exit_price = price
        self.profit = self.quantity * (self.exit_price - self.entry_price)

        # calculate how many 30 day period elapsed between user entering and exiting swap
        elapsed_periods = (self.exited_on - self.entered_on) / (30 * 86400) # 86400 seconds in a day
        self.total_swap_fee = elapsed_periods * self.monthly_fee

        if -1 * self.profit >= self.collateral_value:
            self.is_liquidated = True
            self.treasury_profit = self.total_swap_fee + (self.collateral_value + self.profit)
        else:
            self.treasury_profit = self.total_swap_fee

