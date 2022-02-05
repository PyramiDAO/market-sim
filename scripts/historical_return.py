import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sys
sys.path.append("/Users/zokum/Documents/Workspace/market-sim/scripts/")
from data_feed_v2 import DataFeed

# read in historical ETH price from 2017-08-17 to today, hourly
data_feed = DataFeed("Binance", "ETHUSDT", "1h")
data = data_feed.load_to_df()

'''
Clean up data and get APR
'''
df = data[["unix", "date", "close"]]
df = df.rename(columns={"date": "date time"})
df["date"] = df["date time"].str[:10]
# shift and get price a year ago at this hour
df["close_y"] = df["close"].shift(8760) #there are 365 days in a year, so 8760 hours (yes, simplified, not considering leap year)
df = df.iloc[8760:, :]
# ETH APR is (current price/historica price-1) * 100%
df["ETH APR"] = (df["close"]/df["close_y"] -1)*100

# get average during this period 
avg = df["ETH APR"].mean()
avg_text = f'Average Historical Rolling 1 Year APR for ETH is \n {avg:0.0f}% during this period'
    
'''
Plotting
'''
plt.rcParams.update({'figure.figsize':(15,5), 'figure.dpi':100})

ax = plt.gca()
df.plot(kind='line', x='date', y='ETH APR', color='green', ax=ax)

ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.grid()

ttl = ax.set_title('Historical Rolling ETH 1 Year APR', fontsize=18, pad=18)
ttl.set_position([.5, 1.02])

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
ax.text(0.09, 0.8, avg_text, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig('/Users/zokum/Documents/Workspace/market-sim/scripts/results/historical_1y_APR.png')
plt.show()