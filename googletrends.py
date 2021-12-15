
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

trends = pd.read_csv(r'C:\Users\Teo\Desktop\StockWorld.csv')
trends


djia = yf.download("DJIA", start="2016-12-11", interval="1wk")
#djia = djia[1:861]

#we construct the data and the signals
df = pd.DataFrame()
df["searches"] = trends.Adjusted
df["close"] = djia.reset_index().Close
df["pct_change"] = df.close.pct_change() + 1
df["N"] = df.searches.rolling(window=3).mean().shift(1)
df["n"] = df.searches - df.N
print(df)

df["signal"] = ""

for i, data in enumerate(df.n):
    if data > 0:
        df.loc[i, "signal"] = 1
    else:
        df.loc[i, "signal"] = 0

df = df[3:]
df = df.reset_index()
print(df)


# we construct the portfolio
i = 0
current_port = 100
current_bh = 100
correct = 0
df["portfolio"] = 0
df["buyhold"] = 0
buy_signals = []
sell_signals = []

while i < len(df):
    if df.signal[i] == 0:
        current_port *= df["pct_change"][i]
        buy_signals.append(i)
        if df["pct_change"][i] > 1:
            correct += 1
    else:
        current_port /= df["pct_change"][i]
        sell_signals.append(i)
        if df["pct_change"][i] < 1:
            correct += 1

    current_bh *= df["pct_change"][i]

    df.loc[i, "portfolio"] = current_port
    df.loc[i, "buyhold"] = current_bh

    i += 1

    df["portfolio"].iloc[-1]
print("Annualised Buy-and-Hold Portfolio Return:",
      round(((df["buyhold"].iloc[-1] / 100) ** (1 / (len(df)/52)) - 1) * 100, 1), "%")

print("Accuracy:", round((correct / len(df)) * 100, 1), "%")
print("Total Return:", round((df["portfolio"][len(df)-1] / 100) * 100, 1), "%")
print("Annualised Google Portfolio Return::", round(((df["portfolio"][len(df)-1] / 100) ** (1 / (len(df)/52)) - 1) * 100, 1), "%")

sns.set()

fig, ax = plt.subplots(1, 1, dpi=300)

sns.lineplot(x="index", y="portfolio", data=df, ax=ax,label="Google portfolio")
sns.lineplot(x="index", y="buyhold", data=df, ax=ax, label="Buy and hold portfolio")
ax.legend()
plt.show()

fig, ax = plt.subplots(1, 1, dpi=300)

sns.lineplot(x=df["index"][210:240], y=df["close"], ax=ax)
sns.scatterplot(x=df["index"][210:240], y=df["close"][buy_signals], ax=ax, color="green")
sns.scatterplot(x=df["index"][210:240], y=df["close"][sell_signals], ax=ax, color="red")
plt.show()


