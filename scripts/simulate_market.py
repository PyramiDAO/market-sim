from scripts.data_feed import DataFeed
from scripts.swap_user import SwapUser
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

data_feed = DataFeed("Binance", "ETHUSDT", "1h")
data = data_feed.load_to_df()

EXPOSURE = 1000  # Assumption 0: exposure = 1000$
STARTING_COLLATERAL_PERCENTAGE = 0.05  # Assumption 0: collateral stake = 20% => 200$
STARTING_SWAP_FEE = 0.01  # Assumption 0: fee taken by PyramiDAO = 3% = 30$
verbose = False  # if you want to check each and every user print (not recommended)

cov_result_list = []
var_result_list = []

# this goes reverse cause looks I had missing data in my unix timestamp (so reset_index made the index inverted)
# Assumption 1: 4 users per day => 24 hours per day => 1 user / 6 hours (and as hourly data, should take rows 6 by 6)
# ===> this make 1000$ * 4 = 4000$ of swap volumes per day ===> to be sustained for 30 days
# Assumption 2: 1 row of data = 1 hour => 720 rows = 30 days (which equals the time of the swap agreement)
# Assumption 3: user buys at "high" price of the hour, and sells at "low" price (conservative view)

for COLLATERAL_PERCENTAGE in np.arange(STARTING_COLLATERAL_PERCENTAGE, 0.30, 0.05):

    for SWAP_FEE in np.arange(STARTING_SWAP_FEE, 0.06, 0.01):

        total_treasury_profit = 0
        users_liquidated = 0
        iteration = 0
        fee_perceived = 0
        treasury_coverage = 0
        value_at_risk = 0

        # Loop through DATA dataframe, every 6 hours:
        for unix_time in range(int(data.index[-1]), int(data.index[0]) + 720, -6):
            iteration += 1
            user = SwapUser(EXPOSURE, COLLATERAL_PERCENTAGE, SWAP_FEE)  # create swap user
            unix_entry = unix_time  # not really a unix time anymore but more the index of the DATA dataframe
            entry_price = data_feed.get_market_levels(unix_entry, "high")  # entry price found in DATA
            tx_enter = user.enter_swap(unix_entry, entry_price)
            unix_exit = unix_entry - 720  # find the index in the DATA dataframe 30 days after the user entered the swap
            exit_price = data_feed.get_market_levels(unix_exit, "low")  # close price found in DATA
            tx_exit = user.close_swap(unix_exit, exit_price)

            fee_perceived += user.fee  # sum of the fees perceived by PyramiDAO
            treasury_coverage += user.treasury_profit  # sum of the fees, decreased with the eventual liquidation loss

            # Check Value at risk
            if treasury_coverage[0] < value_at_risk:
                value_at_risk = treasury_coverage[0]

            if verbose:
                if user.is_liquidated:
                    users_liquidated += 1
                    print(
                        f"{iteration}: Liquidated user. Treasury bear a cost of {user.treasury_profit}"
                    )
                else:
                    print(
                        f"{iteration}: User entered swap at {user.entry_price} "
                        f"and closed at {user.exit_price} for profit of {user.profit}"
                    )

        print(f"<li>If fee is {round(SWAP_FEE, 3)} and collateral is {round(COLLATERAL_PERCENTAGE, 2)} "
              f"then VAR is {round(value_at_risk, 2)}</li>")
        var_result_list.append([COLLATERAL_PERCENTAGE, SWAP_FEE, value_at_risk])
        print(f"<li>If fee is {round(SWAP_FEE, 3)} and collateral is {round(COLLATERAL_PERCENTAGE, 2)} "
              f"then coverage is {round(treasury_coverage[0], 2)}</li>")
        cov_result_list.append([COLLATERAL_PERCENTAGE, SWAP_FEE, treasury_coverage[0]])


# Graph VAR vs Treasury P&L ==> this one needs to be run as it's a 3D graph
# Obviously: lowest VAR when fee/collateral are the highest
x, y, z = np.transpose(np.array(var_result_list))
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x, y, z)
plt.show()

# Graph COVERAGE vs Treasury P&L ==> this one needs to be run as it's a 3D graph
# Obviously: higher coverage when fee/collateral are the highest
a, b, c = np.transpose(np.array(cov_result_list))
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(a, b, c)
plt.show()



