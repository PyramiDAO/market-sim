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

<h2>Some results</h2>

<ul>
  <li>The code has run for a combination of collateral (example 0.05 = 5% collateral) and fee (example 0.01 = 1% on the exposure).</li>
  <li>The computation shows the result of VAR (defined as the maximum amount that our treasury needs to cover due to user's loss).</li>
  <li>The computation shows the result of covarage (defined as the sum of fees perceived decreased by eventual use of funds to cover user's loss - ie. our net gain).</li>
</ul>

> RESULTS:
<ul> 
<li>If fee is 0.01 and collateral is 0.05 then VAR is -400695.24</li>
<li>If fee is 0.01 and collateral is 0.05 then coverage is -400695.24</li>
<li>If fee is 0.02 and collateral is 0.05 then VAR is -336655.24</li>
<li>If fee is 0.02 and collateral is 0.05 then coverage is -336655.24</li>
<li>If fee is 0.03 and collateral is 0.05 then VAR is -272615.24</li>
<li>If fee is 0.03 and collateral is 0.05 then coverage is -272615.24</li>
<li>If fee is 0.04 and collateral is 0.05 then VAR is -226651.67</li>
<li>If fee is 0.04 and collateral is 0.05 then coverage is -208575.24</li>
<li>If fee is 0.05 and collateral is 0.05 then VAR is -189131.67</li>
<li>If fee is 0.05 and collateral is 0.05 then coverage is -144535.24</li>
<li>If fee is 0.01 and collateral is 0.1 then VAR is -282908.46</li>
<li>If fee is 0.01 and collateral is 0.1 then coverage is -282908.46</li>
<li>If fee is 0.02 and collateral is 0.1 then VAR is -218868.46</li>
<li>If fee is 0.02 and collateral is 0.1 then coverage is -218868.46</li>
<li>If fee is 0.03 and collateral is 0.1 then VAR is -177287.11</li>
<li>If fee is 0.03 and collateral is 0.1 then coverage is -154828.46</li>
<li>If fee is 0.04 and collateral is 0.1 then VAR is -139767.11</li>
<li>If fee is 0.04 and collateral is 0.1 then coverage is -90788.46</li>
<li>If fee is 0.05 and collateral is 0.1 then VAR is -102247.11</li>
<li>If fee is 0.05 and collateral is 0.1 then coverage is -26748.46</li>
<li>If fee is 0.01 and collateral is 0.15 then VAR is -184452.54</li>
<li>If fee is 0.01 and collateral is 0.15 then coverage is -184452.54</li>
<li>If fee is 0.02 and collateral is 0.15 then VAR is -138540.28</li>
<li>If fee is 0.02 and collateral is 0.15 then coverage is -120412.54</li>
<li>If fee is 0.03 and collateral is 0.15 then VAR is -101056.23</li>
<li>If fee is 0.03 and collateral is 0.15 then coverage is -56372.54</li>
<li>If fee is 0.04 and collateral is 0.15 then VAR is -72168.99</li>
<li>If fee is 0.04 and collateral is 0.15 then coverage is 7667.46</li>
<li>If fee is 0.05 and collateral is 0.15 then VAR is -53677.73</li>
<li>If fee is 0.05 and collateral is 0.15 then coverage is 71707.46</li>
<li>If fee is 0.01 and collateral is 0.2 then VAR is -114237.66</li>
<li>If fee is 0.01 and collateral is 0.2 then coverage is -108287.41</li>
<li>If fee is 0.02 and collateral is 0.2 then VAR is -76847.66</li>
<li>If fee is 0.02 and collateral is 0.2 then coverage is -44247.41</li>
<li>If fee is 0.03 and collateral is 0.2 then VAR is -51770.28</li>
<li>If fee is 0.03 and collateral is 0.2 then coverage is 19792.59</li>
<li>If fee is 0.04 and collateral is 0.2 then VAR is -33348.44</li>
<li>If fee is 0.04 and collateral is 0.2 then coverage is 83832.59</li>
<li>If fee is 0.05 and collateral is 0.2 then VAR is -14928.44</li>
<li>If fee is 0.05 and collateral is 0.2 then coverage is 147872.59</li>
<li>If fee is 0.01 and collateral is 0.25 then VAR is -68246.33</li>
<li>If fee is 0.01 and collateral is 0.25 then coverage is -53533.48</li>
<li>If fee is 0.02 and collateral is 0.25 then VAR is -39628.33</li>
<li>If fee is 0.02 and collateral is 0.25 then coverage is 10506.52</li>
<li>If fee is 0.03 and collateral is 0.25 then VAR is -21221.66</li>
<li>If fee is 0.03 and collateral is 0.25 then coverage is 74546.52</li>
<li>If fee is 0.04 and collateral is 0.25 then VAR is -2821.66</li>
<li>If fee is 0.04 and collateral is 0.25 then coverage is 138586.52</li>
<li>If fee is 0.05 and collateral is 0.25 then VAR is -305.33</li>
<li>If fee is 0.05 and collateral is 0.25 then coverage is 202626.52</li>
</ul>
