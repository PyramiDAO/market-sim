# market-sim
Market Simulation for PyramiDAO protocol

<h1> PyramiDAO </h1>
What does PyramiDAO do?
  <ul>
    <li>Facilitating Total Return Swap (TRS) to let user get leveraged exposure to underlying assets, in exchange, we charge a fixed swap fee</li>
    <li>PyramiDAO will have various Vaults, corresponding to various Strategies, i.e., underlying assets user wants leveraged exposure to</li>
    <li>Profit Treasury vaults earn will be distributed to PyramiDAO token holders as a percent</li>
  </ul>

<h1>Assumptions</h1>
Here is a list of assumptions on which the sim is built
  <ul>
    <li>The user enters a swap with the Treasury (hence the treasury assets)</li>
    <li>Treasury always approves the TRS once user requests</li>
    <li>User has to put down a certain percent collateral</li>
    <li>PyramiDAO utlizes Chainlink Oracle to check for asset prices periodically, if price of assets falls below the collateral, then user gets force liquidated</li>
    <li>User can choose to enter and exit TRS contract at will</li>
    <li>This simulation currently simulates for only one Vault -- the strategy to invest in ETH</li>
  </ul>

<h1>How Simulation was Conducted</h1>
Basic set up
  <ul>
    <li>pyramiDAO.py is the entry point for simulation</li>
    <li>N_SIM defines the number of simulations run for a set of parameters (more details on paramters below), for our result, we simulate for at least 500 iterations</li>
    <li>At the beginning of the simulation, a random seed is set</li>
  </ul>

<h1>Parameters for the Simulation</h1>
Parameters for turning 
  <ul>
      <li>PERIOD_START, PERIOD_END: these two parameters define the historical period the simulation is run upon. This helps us simulate for especially distresed historical period </li>
      <li>  For the result below, we simulated for (1)2021 summer dip: 2021-05-07 to 2021-07-18 (2)2020 covid dip: 2020-02-01 to 2020-04-01 and (3)Normal: 2017-08 to 2022-02</li>
      <li>COLLATERAL_PERCENTAGE: required collateral (in percent) of the exposure user wants to enter TRS on</li>
      <li>  The goal is to have enough collateral but also allow users to have as much leverage as possible</li>
      <li>SWAP_FEE: a fixed rate user pays PyramiDAO in this TRS, period is 30 days</li>
      <li>LIQUIDATE_PERIOD: the period in which PyramiDAO checks the current price of asset against the collateral, and trigger force liquidation if price drops below what collateral can cover and end the TRS</li>
      <li>  For simulation we picked 24 hours, i.e. checking the asset price every day</li>
  </ul>
Randomzed paramters
  <ul>
    <li>NUM_USERS: random integer from uniform distribution between 100 and 20,000</li>
    <li>EXPOSURE: random floating number from exponential distribution, with floor of $100.0</li>
    <li>rand_exit, rand_entry: utilizing a uniform distribution to simulate user randomly entering and exiting swap during the given period we are simulating</li>
  </ul>


<h1>Results</h1>
  <ul>
    <li>Our result shows that during various market conditions, give the mechanism we described above (especially period Oracle checking and force liquidation, combined with required collateral), PyramiDAO Treasury will be able to make consistent profit, while providing users with very effective leverage </li>
    <li>LIQUIDATE_PERIOD is very important, when the market is very volatile, we must increase the frequency PyramiDAO is checking Chainlink Oracle price against collateral</li>
    <li>During the summer dip for ETH in 2021 (2021-05-07 to 2021-07-18)</li>
    <li>  20% collateral, 1% swap fee: 95% VaR = $34,249, 99% VaR = $12,085</li>
    <li>  10% collateral, 1% swap fee: 95% VaR = $15,538, 99% VaR = $6,456</li>
    <li>  7% collateral, 1% swap fee: 95% VaR = $9,356, 99% VaR = $610</li>
    <li>  6% collateral, 1% swap fee: 95% VaR = $1,518, 99% VaR = ($2,654)</li>
    <li>  5% collateral, 1% swap fee: 95% VaR = ($5,580), 99% VaR = ($11,666)</li>
    <li>During the Covid dip for ETH in 2020 (2020-02-01 to 2020-05-01)</li>
    <li>  20% collateral, 1% swap fee: 95% VaR = $572, 99% VaR = $3.89</li>
    <li>  10% collateral, 1% swap fee: 95% VaR = ($152,329), 99% VaR = ($162.720)</li>
    <li>  5% collateral, 1% swap fee: 95% VaR = ($8,795), 99% VaR = ($13,853)</li>
    <li>During the entirety of our historica data (2017-08 to 2022-02)</li>
    <li>  10% collateral, 1% swap fee: 95% VaR = $730,611, 99% VaR = $213.433</li>
  </ul>

How to interpret Value at Risk?
  <ul>
    <li>VaR is the maximum amount at risk to be lost (1) over a period of time (2) at a particular level of confidence</li>
    <li>For example, if during the summer dip for ETH in 2021 (2021-05-07 to 2021-07-18), the 95% VaR is -$5,580, then that means, with 95 probability, PyramiDAO will not lose more than $5,580 by facilitating TRS during the given period
</li>
    <li>As we can see from results above, most of the time our simulation actually makes a profit still, with reasonable </li>

  </ul>

    
        
        