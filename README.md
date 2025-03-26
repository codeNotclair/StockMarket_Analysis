# StockMarket_Analysis
The Indian Stock Market Analysis Tool fetches stock data from NSE/BSE, checks if today’s closing price lies within yesterday’s open-close range, and saves matching stocks in an Excel file. It uses Python, pandas, yfinance/NSEpy, and automates execution via cron jobs. Ideal for tracking stable stock movements efficiently

How It Works:
✅ Fetches NSE stock tickers dynamically from the official NSE stock list.
✅ Retrieves historical stock data using Yahoo Finance (yfinance).
✅ Checks if today’s closing price falls between yesterday’s opening and closing prices.
✅ Applies additional conditions (if today's high/low stays within yesterday's high/low).
✅ Saves results in a CSV file (indian_stock_analysis.csv).

Technologies Used:
🔹 Python, pandas, yfinance – Data fetching & analysis
🔹 ThreadPoolExecutor – Multithreading for faster processing
🔹 CSV file handling – Stores results efficiently

Features:
📊 Analyzes all NSE-listed stocks
📉 Filters stocks meeting specific conditions
📝 Creates a structured CSV report
⚡ Optimized with multi-threading
🕒 Automatable using cron jobs
