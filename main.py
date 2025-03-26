import yfinance as yf
import pandas as pd
import os
import csv
import time
from concurrent.futures import ThreadPoolExecutor

def get_nse_stock_list():
    """Fetches all NSE stock tickers dynamically from NSE's official stock list CSV."""
    try:
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        df = pd.read_csv(url)
        
        if "SYMBOL" not in df:
            print("⚠️ Error fetching stock list: No SYMBOL column found.")
            return []
        
        tickers = [symbol.strip() + ".NS" for symbol in df["SYMBOL"].dropna()]
        return tickers
    except Exception as e:
        print(f"⚠️ Error fetching stock list: {e}")
        return []

def get_stock_data(ticker):
    """Fetches stock data for the last two days with retries on failure and adds a delay to avoid rate limiting."""
    for attempt in range(3):
        try:
            time.sleep(1)  
            stock = yf.Ticker(ticker)
            data = stock.history(period="3d")
            
            if len(data) < 2:
                return None

            return data.iloc[-3:-1]
        except Exception as e:
            time.sleep(2)
    return None

def analyze_stock(ticker):
    """Checks stock conditions and returns results if condition matches."""
    data = get_stock_data(ticker)
    
    if data is None or len(data) < 2:
        return None

    yesterday = data.iloc[-1]
    time.sleep(1)
    today = yf.Ticker(ticker).history(period="1d")

    if today.empty:
        return None

    today_close = today['Close'].values[0]
    today_high = today['High'].values[0]
    today_low = today['Low'].values[0]
    
    yesterday_open = yesterday['Open']
    yesterday_close = yesterday['Close']
    yesterday_high = yesterday['High']
    yesterday_low = yesterday['Low']

    result = "Within Range" if yesterday_open <= today_close <= yesterday_close else "Out of Range"
    extra_condition = "Matches Condition" if (today_high < yesterday_high and today_low > yesterday_low) else "Doesn't Match"
    
    if extra_condition == "Matches Condition":
        return [ticker, round(yesterday_open, 2), round(yesterday_close, 2), round(today_close, 2), round(yesterday_high, 2), round(yesterday_low, 2), round(today_high, 2), round(today_low, 2), result, extra_condition]
    else:
        return None

def save_to_csv(results):
    """Saves stock analysis results to a CSV file."""
    filename = "indian_stock_analysis.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Ticker", "Yesterday Open (₹)", "Yesterday Close (₹)", "Today Close (₹)", "Yesterday High (₹)", "Yesterday Low (₹)", "Today High (₹)", "Today Low (₹)", "Result", "Condition Check"])
        writer.writerows(results)

def analyze_all_nse_stocks():
    """Fetches all NSE stock tickers and analyzes them using limited multithreading to prevent rate limiting."""
    tickers = get_nse_stock_list()
    
    if not tickers:
        print("⚠️ No NSE stock tickers found. Check the NSE website.")
        return
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:  # Reduced concurrent workers to prevent rate limiting
        results = list(filter(None, executor.map(analyze_stock, tickers)))
    
    if results:
        save_to_csv(results)
    else:
        print("No stocks matched the condition.")

if __name__ == "__main__":
    analyze_all_nse_stocks()
