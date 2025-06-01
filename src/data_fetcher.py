# Import required libraries
# requests: for making HTTP requests to the Binance API
# pandas: for handling data in table format
# datetime: for working with dates and times
# typing: for adding type hints to make code more readable
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

class BinanceDataFetcher:
    """
    A class that downloads historical price data from Binance cryptocurrency exchange.
    
    This class handles:
    1. Connecting to Binance's API
    2. Downloading candlestick (OHLCV) data
    3. Converting the data into a format we can use
    """
    
    # The base URL for Binance's klines (candlestick) API endpoint
    BASE_URL = "https://api.binance.com/api/v3/klines"
    
    def __init__(self):
        """
        Initialize the data fetcher.
        Creates a session that we'll reuse for all API calls (this is more efficient).
        """
        self.session = requests.Session()
    
    def fetch_klines(self, symbol: str, interval: str = "1m", limit: int = 5000) -> pd.DataFrame:
        """
        Download candlestick data from Binance.
        
        Parameters:
        -----------
        symbol : str
            The trading pair to fetch data for (e.g., 'BTCUSDT' for Bitcoin/USDT)
        interval : str
            The time period for each candle (default: '1m' for 1 minute)
        limit : int
            How many candles to fetch (default: 5000, which is Binance's maximum)
        
        Returns:
        --------
        pandas.DataFrame
            A table containing the OHLCV data with columns:
            - open: Opening price for the period
            - high: Highest price during the period
            - low: Lowest price during the period
            - close: Closing price for the period
            - volume: Trading volume during the period
        """
        # Prepare the parameters for our API request
        params = {
            "symbol": symbol.upper(),  # Convert symbol to uppercase (Binance requires this)
            "interval": interval,
            "limit": limit
        }
        
        # Make the API request and check for errors
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()  # This will raise an error if the request failed
        
        # Convert the JSON response into a pandas DataFrame
        # Binance returns data as a list of lists, so we need to specify column names
        data: List[List[Any]] = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades_count',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        
        # Convert the timestamp from milliseconds to a datetime object
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Convert price and volume columns from strings to floating point numbers
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        # Set the timestamp as the index of our DataFrame
        # This makes it easier to align data when calculating indicators
        df.set_index('timestamp', inplace=True)
        
        # Return only the columns we need for backtesting
        return df[['open', 'high', 'low', 'close', 'volume']]

    def __del__(self):
        """
        Cleanup method that runs when the object is destroyed.
        Makes sure we properly close the network session.
        """
        self.session.close() 