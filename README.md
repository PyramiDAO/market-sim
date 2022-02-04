# market-sim
Market Simulation for liquidation and treasury P&amp;L

<h1>Assumptions</h1>
Here is a list of assumptions on which the sim is built.
  <ul>
    <li>The user enters a swap with the Treasury (hence the treasury assets)</li>
    <li>The contract is fixed for 30 days</li>
    <li>There is no liquidation done during the 30 days period (this solves some issues, I guess), but the liquidation occurs at the end of the 30 in proportion of the assets effectively lost at the closing.</li>
    <li>This involves that the % collateral might not be sufficient to cover users loss</li>
  </ul>

<h1>How to use</h1>
  <ul>
    <li>Install: numpy / pandas / matplotlib / ssl</li>
    <li>Run the simulate_market.py script</li>
  </ul>

<h1>Summary</h1>
Based on the assumptions above, if there is a constant flow of users swapping 4000$ total per day for a period of 30 days, we need: 4000$ * 30 days = 120,000$ in our treasury to sustain such volumes. Based on the curve plotted, we need a fee of approx 3% (and a collateral of 20%) to ensure such a business model is profitable for the treasury (based on full market cycle from 2017 till today).
