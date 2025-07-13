# 📈 Momentum Analysis for Stock Tickers

Ever wondered which stocks quietly crush it month after month? This script helps you find out.

This project analyzes historical stock data to uncover monthly momentum patterns for tickers using Yahoo Finance. It calculates total return, average monthly return, and consistency of positive performance, then outputs everything to clean, human-readable CSVs.

---

## How to Run It

Make sure you have Python 3 installed.

### 1. Clone the repo and navigate into it:
```bash
git clone https://github.com/rshah-42/momentum-analysis.git
cd momentum-analysis
```

### 2. Set up your virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Run the script:
```bash
python3 momentum_analysis.py
```

---

## What Gets Created?

Running the script will generate the following files:

1. **`monthly_momentum.csv`**  
   → A long-format DataFrame with monthly returns for each ticker and date.

2. **`momentum_spikes.csv`**  
   → A count of how many months each stock had a return greater than 5% (momentum spikes).

3. **`ranked_stocks.csv`**  
   → A ranked list of all tickers sorted by:
   - Total 12-month return
   - Number of month-to-month increases (consistency)
   - Average monthly return

---

## What's Inside?

- `momentum_analysis.py` – The main script that does all the work
- `requirements.txt` – Contains:
  - `pandas` for data manipulation
  - `yfinance` for fetching historical price data
- `tickers.csv` – The list of example stock tickers to analyze. You can replace it with your own list, but it must be present in your working directory

---

## Notes

- This project uses monthly-adjusted close prices.
- A 2-second pause is added between download batches to avoid hitting Yahoo Finance's rate limits.
- You may change the timeframe depending on how far back you would like to analyze your stocks. 

---

Made with 🧠 and Python.
