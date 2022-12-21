import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime

csv_output_path = "/Users/hari/Documents/Hari_Python_Projects/risk-reward-simulator/simulations_csv/"
plots_output_path = "/Users/hari/Documents/Hari_Python_Projects/risk-reward-simulator/plots/"
mode = 1  # 1 == fixed risk in RUPEES, 2 == as a % of capital


ACCOUNT_PROFITS = []
sim_result = []


def simulate(account_size, total_trades, risk_per_trade, win_rate, risk_reward):
    global ACCOUNT_PROFITS, NEW_ACCOUNT_PROFITS
    equity = account_size
    accounts = [equity]

    # below creating an array of length 'total_trades' containing random numbers between 1 and 100
    outcomes = list(np.round(np.random.uniform(1, 101, total_trades), 2))
    for i in range(len(outcomes)):
        trade = outcomes[i]
        win = trade <= win_rate  # If trade < W%, winner :
        if mode == 1:  # Fixed risk in Rupees
            risk = -1 * (risk_per_trade)
        if mode == 2:  # Risk as a % of capital
            risk = -1 * np.round(equity * risk_per_trade / 100, 2)
        profit_per_trade = abs(risk) * risk_reward
        profit = profit_per_trade if win else risk
        equity += profit
        accounts.append(equity)

    ACCOUNT_PROFITS.append(accounts)
    [NEW_ACCOUNT_PROFITS] = ACCOUNT_PROFITS


# |---------|---------|---------| < Set values of parameters here >|---------|---------|---------|
account_size = 500000  # starting capital equity
total_trades = 250  # total trades in each simulation
# how much we are willing to lose in a losing trade
if mode == 1:
    risk_per_trade = 5000  # fixed risk in RUPEES
if mode == 2:
    risk_per_trade = 1  # as a % of capital
# % of trade count that is winner
win_rate = 30
# How much on average a winning trades earn compared to average losing trade
risk_reward = 4

# how many iterations of simulation should be run
total_sims = 100

for i in range(total_sims):
    simulate(account_size, total_trades, risk_per_trade, win_rate, risk_reward)
    sim_result.append(NEW_ACCOUNT_PROFITS)
    ACCOUNT_PROFITS.clear()

df = pd.DataFrame(sim_result)  # Convert to DataFrame

currtime = datetime.datetime.now()
now_time = currtime.strftime("%Y") + currtime.strftime("%m") + currtime.strftime(
    "%d") + currtime.strftime("%H") + currtime.strftime("%M") + currtime.strftime("%S")

print("SAVING CSV")
tocsv_filename = "sim_result_" + now_time + "_WR_" + str(win_rate) + "_RR_" + str(
    risk_reward) + "_RPT_" + str(risk_per_trade) + "_SIMS_" + str(total_sims) + "_MODE_" + str(mode) + ".csv"

df.to_csv(csv_output_path + tocsv_filename)

# Transpose the DF
df2 = pd.DataFrame.transpose(df)

fig = plt.figure()
plt.plot(df2)
plt.ticklabel_format(useOffset=False, style='plain')

# axis title
sim_count = (total_trades)
label_yaxis = df[sim_count].max()
label_yaxis -= 100000

plt.xlabel("Trades")
plt.ylabel("P/L")

plt.text(10, label_yaxis, f'{now_time}, \n WR: {win_rate}, RR: {risk_reward}, RPTrd: {risk_per_trade}, SIMS: {total_sims}, MODE: {mode}',
         fontsize=7, bbox=dict(facecolor="red", alpha=0.5),)

plt.hlines(y=500000, xmin=0, xmax=total_trades, linewidth=2, color='k')

plt.grid()

print("SAVING PLOT\n")

plt.savefig(plots_output_path + now_time + "_WR_" + str(win_rate) + "_RR_" + str(risk_reward) + "_RPT_" +
            str(risk_per_trade) + "_SIMS_" + str(total_sims) + "_MODE_" + str(mode) + ".png", format="png", dpi=512, bbox_inches="tight",)
print(f"Capital = {account_size}")
print(f"Total Trades = {total_trades}")
if mode == 1:
    print(f"Risk Per Trade = {risk_per_trade} Rupees")
elif mode == 2:
    print(f"Risk Per Trade = {risk_per_trade} %")
print(f"Win-Rate % = {win_rate}")
print(f"Risk : Reward = 1 : {total_trades}")
print(f"Total Simulations = {total_sims}")

print(" ---------- DONE ---------- ")
