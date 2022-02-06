import sys
sys.path.append("/Users/zokum/Documents/Workspace/market-sim/scripts/")
from data_feed_v2 import DataFeed
from swap_user_v2 import SwapUser
from treasury import Treasury
import random
import time
from math import floor
import pandas as pd
from multiprocessing import Process
import matplotlib.pyplot as plt

def run_sim(COLLATERAL_PERCENTAGE, SWAP_FEE, LIQUIDATE_PERIOD, sim_start, sim_end, data, simulation_result_queue):
    # todo delete
    # temp = []
    for _ in range(sim_start, sim_end):
        # TODO should be correlated with market condition and our token prices and everything 
        NUM_USERS = random.randint(100, 20_000) # number of users during a simulation period; for now just a uniform distribution until we get more info
        fee_received = 0
        treasury_coverage = 0
        num_liquidated = 0

        for _ in range(NUM_USERS):

            EXPOSURE = max(random.expovariate(1/1000), 100.0)  # amount of underlying assets user wants exposure on, in $; exponential distribution because most users will want to try a little bit of money only; force the floor to be $100
            
            user = SwapUser(EXPOSURE, COLLATERAL_PERCENTAGE, SWAP_FEE)  # create swap user
            rand_exit = random.randint(0, len(data)-1) # randomly find the exit point, so we can find the entry, which should always come before exit point
            rand_entry = random.randint(0, rand_exit) # randomly find the entry point, with exit being the right limit
            
            user.enter_swap(data.iloc[rand_entry, 0], (data.iloc[rand_entry, 4] + data.iloc[rand_entry, 5])/2) # use simple average of high and low prices during the hour as the price of entry
            
            # simulate reconciliation, if user's collateral is not enough to cover for the dip in price, we force liquidate
            for i in range(rand_entry+LIQUIDATE_PERIOD, rand_exit, LIQUIDATE_PERIOD):
                diff = (data.iloc[i, 4] + data.iloc[i, 5])/2  - (data.iloc[i-24, 4] + data.iloc[i-24, 5])/2
                if -1 * diff >= user.collateral_value:
                    user.force_liquidated(data.iloc[i, 0], (data.iloc[i, 4] + data.iloc[i, 5])/2)  
                    break   

            if not user.is_liquidated: # only close swap when if user has not been force liquidated
                user.close_swap(data.iloc[rand_exit, 0], (data.iloc[rand_exit, 4] + data.iloc[rand_exit, 5])/2) # use simple average of high and low prices during the hour as the price of exit
            else: 
                num_liquidated += 1

            fee_received += user.total_swap_fee  # sum of the fees perceived by PyramiDAO
            treasury_coverage += user.treasury_profit  # sum of the fees, decreased with the eventual liquidation loss

        #     print(user.exit_price)
        #     print(user.entry_price)
        # print(user.treasury_profit)
        # temp.append(treasury_coverage)

        simulation_result_queue.put(treasury_coverage)
        print(f"{NUM_USERS} users in this iteration, {num_liquidated} got liquidated, ETH vault ended with ${treasury_coverage:,.2f}")

if __name__ == "__main__":
    # set random seed for reproducibility 
    random.seed(890)
    # set how many processors to run this simulation with (should be at least 1 less than the actual CPUs on your computer)
    NUM_PROC = 7
    # !#### set the number of simulations to run for 
    N_SIM = 500

    # read in historical ETH price from 2017-08-17 to today, hourly
    data_feed = DataFeed("Binance", "ETHUSDT", "1h")
    data = data_feed.load_to_df()
    # add an actual datetime day column to help pick which historical period to simulate for
    data["day"] = data["date"].str[:10]
    data["day"] = pd.to_datetime(data["day"], infer_datetime_format=True)

    # ! #### pick stressful (bad) period to simulate for
    # PERIOD_START, PERIOD_END = '2020-01-01', '2020-05-01' # COVID dip
    # period = 'covidDip2020'
    # PERIOD_START, PERIOD_END = '2021-05-07', '2021-07-18' # 2021 summer dip
    # period = 'summperDip2021'
    PERIOD_START, PERIOD_END = '2017-08-17', '2022-02-05'
    period = '2020AugTo2022Feb'
    data = data.loc[(data['day'] > PERIOD_START) & (data['day'] < PERIOD_END)]

    # !#### play with different collateral  
    COLLATERAL_PERCENTAGE = 0.10
    # !#### monthly fixed rate user pays PyramiDAO in this return swap, in exchange for us providing them with leverage to get exposure
    SWAP_FEE = 0.01
    # !#### pick how often you want to use Chainlink to check ETH prices
    LIQUIDATE_PERIOD = 24

    # make our treasury with no money in it
    # TODO: stretch goal: we should change this param later 
    treasury = Treasury(0.0)

    # TODO: stretch goal: incorporate in token profit sharing
    PROFIT_SHARE_PERIOD = 1
    DIVIDEND = 0.01 # amount of profit sharing to token holders when Treasury makes profit 


    
    jobs = []
    nums = N_SIM // NUM_PROC
    tic = time.perf_counter()

    for i in range(NUM_PROC):
        sim_start = i*nums
        if i == NUM_PROC-1:
            sim_end = N_SIM
        else:
            sim_end = i*nums + nums

        process = Process(
                target=run_sim, 
                args=(COLLATERAL_PERCENTAGE, SWAP_FEE, LIQUIDATE_PERIOD, sim_start, sim_end, data, treasury.get_simulation_result_queue())
            )
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    toc = time.perf_counter()
    print(f"Running {N_SIM} simulations took {toc - tic:0.4f} seconds")


    sim_output = [] 
    print("\nstarting to collect all simulation results...")
    for _ in range(N_SIM):
        sim_output.append(treasury.simulation_result_queue.get())

    # calculate 95% and 99% VaR
    ''''
    interpretation: with 95 or 99% probability, PyramiDAO will not lose more than X amount $ by facilitating TRS during the given period
    VaR is the maximum amount at risk to be lost
        over a period of time
        at a particular level of confidence
    '''
    # sort first
    sim_output = sorted(sim_output)
    var95 = sim_output[floor(len(sim_output)*0.05)]
    var99 = sim_output[floor(len(sim_output)*0.01)]

    # plot histogram of this run of simulations
    plt.rcParams.update({'figure.figsize':(11,7), 'figure.dpi':100})
    ax = plt.gca()
    plt.hist(sim_output, bins=30)
    plt.gca().set(
        xlabel='ETH Vault Price ($)',
        ylabel='Frequency'
    )
    ttl = ax.set_title(
        f'''ETH Vault Gain/Loss Distribution \n 
        {N_SIM} Simulations with {SWAP_FEE*100:0.0f}% Monthly Swap Fee and {COLLATERAL_PERCENTAGE*100:0.0f}% Collateral \n 
        (Period: {PERIOD_START} to {PERIOD_END})''', 
        fontsize=12, 
        pad=18
    )

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    ax.text(0.01, 0.95, f'95% VaR = ${var95:,.2f} \n99% VaR = ${var99:,.2f}', transform=ax.transAxes, fontsize=14, 
            verticalalignment='top', bbox=props)

    plt.gca().set_xticklabels(['${:,.2f}'.format(x)
                               for x in plt.gca().get_xticks()])

    output_filename = f'/Users/zokum/Documents/Workspace/market-sim/results/{N_SIM}_sims_{COLLATERAL_PERCENTAGE*100:0.0f}%_collateral_{SWAP_FEE*100:0.0f}%_swapfee_{period}.png'
    plt.savefig(output_filename)
    # plt.show()

    


