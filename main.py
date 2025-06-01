import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Backtester:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.position = 0
        self.cash = 100000  # Initial capital
        self.portfolio_value = []
        
    def fetch_data(self):
        """Fetch historical data from Yahoo Finance"""
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        return self.data
    
    def run_strategy(self):
        """Implement your trading strategy here"""
        pass
    
    def calculate_metrics(self):
        """Calculate performance metrics"""
        pass

def main():
    # Example usage
    symbol = "AAPL"  # Example stock
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Last 1 year of data
    
    backtester = Backtester(symbol, start_date, end_date)
    data = backtester.fetch_data()
    print(f"Loaded {len(data)} days of data for {symbol}")

if __name__ == "__main__":
    main() 