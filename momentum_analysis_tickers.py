import pandas as pd
import yfinance as yf
import datetime
import time

#STEP 1: Load Tickers

# Read tickers from a CSV file. The file should have one ticker per row.
tickers_df = pd.read_csv("tickers.csv", header=None, names=["Ticker"])
tickers = tickers_df["Ticker"].dropna().unique().tolist()

tickers = ["BRK-B" if t == "BRKB" else t for t in tickers]

print(f"✅ Loaded {len(tickers)} tickers")
print("Sample tickers:", tickers[:10])

#STEP 2: Set Time Range
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=390)

# Break tickers into smaller groups to avoid download issues
batch_size = 50
all_results = []

#STEP 3: Download and Process Each Batch

for i in range(0, len(tickers), batch_size):
    batch = tickers[i:i + batch_size]
    print(f"\n⬇️ Downloading batch: {batch}")

    try:
        # Download monthly adjusted close prices
        data = yf.download(
            tickers=batch,
            start=start_date,
            end=end_date,
            interval="1mo",
            auto_adjust=True,
            group_by="ticker",
            progress=False
        )

        # Handle single ticker case
        if len(batch) == 1:
            ticker = batch[0]
            if 'Close' not in data.columns:
                print(f"❌ No 'Close' data for {ticker}, skipping.")
                continue
            close_prices = data['Close'].to_frame(name=ticker)

        # Handle multiple tickers with multi-level column index
        elif isinstance(data.columns, pd.MultiIndex) and 'Close' in data.columns.get_level_values(1):
            close_prices = data.xs('Close', level=1, axis=1)
        else:
            print("❌ 'Close' prices not found in data, skipping batch.")
            continue

        # Calculate monthly returns
        monthly_returns = close_prices.pct_change().dropna()

        # Convert wide format to long format
        melted = monthly_returns.reset_index().melt(
            id_vars="Date",
            var_name="Ticker",
            value_name="Monthly Return"
        )

        all_results.append(melted)
        time.sleep(2)  # Wait to avoid rate-limiting

    except Exception as e:
        print(f"❌ Error downloading batch: {batch}")
        print(str(e))
        continue

#STEP 4: Combine and Save Data

if not all_results:
    print("⚠️ No data was collected. Please check ticker list or internet connection.")
    exit()

# Combine all batches into one DataFrame
returns_df = pd.concat(all_results, ignore_index=True)
returns_df.sort_values(by=["Ticker", "Date"], inplace=True)

# Save monthly returns to CSV
returns_df.to_csv("monthly_momentum.csv", index=False)
print("\n📁 Saved: monthly_momentum.csv")
print(returns_df.head())

#STEP 5: Analyze Momentum

# 1. Count how many months each stock had > 5% return
spikes = (
    returns_df[returns_df["Monthly Return"] > 0.05]
    .groupby("Ticker")
    .size()
    .reset_index(name="Months > 5% Return")
)
spikes.sort_values(by="Months > 5% Return", ascending=False, inplace=True)
spikes.to_csv("momentum_spikes.csv", index=False)
print("\n📁 Saved: momentum_spikes.csv")
print(spikes.head())

# 2. Calculate 12-month total return per stock
total_return = (
    returns_df.groupby("Ticker")["Monthly Return"]
    .apply(lambda x: (1 + x).prod() - 1)
    .reset_index(name="12-Month Return")
)

# 3. Calculate average monthly return
avg_return = (
    returns_df.groupby("Ticker")["Monthly Return"]
    .mean()
    .reset_index(name="Average Monthly Return")
)

# 4. Count number of months where return increased from previous month
def count_upward_trends(series):
    return sum(earlier < later for earlier, later in zip(series, series[1:]))

month_to_month = (
    returns_df.sort_values(["Ticker", "Date"])
    .groupby("Ticker")["Monthly Return"]
    .apply(count_upward_trends)
    .reset_index(name="Month-to-Month Increases")
)

#STEP 6: Combine Metrics and Rank

ranking = (
    total_return
    .merge(avg_return, on="Ticker")
    .merge(month_to_month, on="Ticker")
)

# Sort by total return and consistency
ranking = ranking.sort_values(
    by=["12-Month Return", "Month-to-Month Increases"],
    ascending=False
)

# Save to CSV
ranking.to_csv("ranked_stocks.csv", index=False)
print("\n📁 Saved: ranked_stocks.csv")
print(ranking.head())