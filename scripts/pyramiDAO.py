import sys
sys.path.append("/Users/zokum/Documents/Workspace/market-sim/scripts/")
from data_feed_v2 import DataFeed
from swap_user_v2 import SwapUser
from treasury import Treasury
import numpy as np
from datetime import datetime
import random
import time
from multiprocessing import Process
import matplotlib.pyplot as plt

def run_sim(COLLATERAL_PERCENTAGE, SWAP_FEE, sim_start, sim_end, data, simulation_result_queue):
    for _ in range(sim_start, sim_end):
        fee_perceived = 0
        treasury_coverage = 0

        # TODO should be correlated with market condition and our token prices and everything 
        NUM_USERS = random.randint(100, 20_000) # number of users during a simulation period; for now just a uniform distribution until we get more info
        
        for _ in range(NUM_USERS):

            EXPOSURE = random.expovariate(1/1000) # amount of underlying assets user wants exposure on, in $; exponential distribution because most users will want to try a little bit of money only
            
            # create swap user
            user = SwapUser(EXPOSURE, COLLATERAL_PERCENTAGE, SWAP_FEE)  # create swap user
            try:
                rand_exit = random.randint(0, len(data)-1) # randomly find the exit point, so we can find the entry, which should always come before exit point
                rand_entry = random.randint(0, rand_exit) # using 24 to force the gap to be bigger
                user.enter_swap(data.iloc[rand_entry, 0], (data.iloc[rand_entry, 4] + data.iloc[rand_entry, 5])/2) # use simple average of high and low prices during the hour as the price of entry
                # TODO: priority -- implement something to rebalance and liquidate every hour if collateral is not enough to cover
                user.close_swap(data.iloc[rand_exit, 0], (data.iloc[rand_exit, 4] + data.iloc[rand_exit, 5])/2) # use simple average of high and low prices during the hour as the price of exit

                fee_perceived += user.fee  # sum of the fees perceived by PyramiDAO
                treasury_coverage += user.treasury_profit  # sum of the fees, decreased with the eventual liquidation loss
            except Exception as e:
                print("rand_exit=", rand_exit)
                print("rand_entry=", rand_entry)
                print(e)

        simulation_result_queue.put(treasury_coverage)
        print("# of users in this iteration is", NUM_USERS, ", treasury reserved is now at", treasury_coverage)

if __name__ == "__main__":
    # set random seed for reproducibility 
    random.seed(890)
    # set how many processors to run this simulation with (should be at least 1 less than the actual CPUs on your computer)
    NUM_PROC = 7
    # set the number of simulations to run for 
    N_SIM = 500 

    # make our treasury with no money in it
    # TODO we should change this param later 
    treasury = Treasury(0.0)
    
    COLLATERAL_PERCENTAGE = 0.5
    SWAP_FEE = 0.03

    # TODO
    PROFIT_SHARE_PERIOD = 1
    DIVIDEND = 0.01 # amount of profit sharing to token holders when Treasury makes profit 

    # read in historical ETH price from 2017-0817 to today, hourly
    data_feed = DataFeed("Binance", "ETHUSDT", "1h")
    data = data_feed.load_to_df()

    
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
                args=(COLLATERAL_PERCENTAGE, SWAP_FEE, sim_start, sim_end, data, treasury.get_simulation_result_queue())
            )
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    toc = time.perf_counter()
    print(f"Running {N_SIM} simulations took {toc - tic:0.4f} seconds")


    sim_output = [] 
    for _ in range(N_SIM):
        sim_output.append(treasury.simulation_result_queue.get())

    # plot histogram of this run of simulations
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})
    plt.hist(sim_output, bins=20)
    plt.gca().set(
        title='Gain/Loss Distribution', 
        xlabel='Treasury Reserve Distribution ($)',
        ylabel='Count'
    )
    plt.show()

    output_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'/Users/zokum/Documents/Workspace/market-sim/results/{N_SIM}_sims_{COLLATERAL_PERCENTAGE}_collateral_{SWAP_FEE}_swapfee_{output_timestamp}.png'
    plt.savefig(output_filename)


