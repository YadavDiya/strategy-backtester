# Import required libraries
# pandas: for data manipulation and calculations
# numpy: for numerical operations (though not directly used, it's used by pandas)
# typing: for type hints to make code more readable
import pandas as pd
import numpy as np
from typing import Tuple

def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """
    Calculate the Exponential Moving Average (EMA) of a price series.
    
    EMA gives more weight to recent prices, making it more responsive to new information
    than a simple moving average (SMA).
    
    Parameters:
    -----------
    data : pd.Series
        The price series to calculate EMA for (usually closing prices)
    period : int
        The number of periods to use in the EMA calculation
        
    Returns:
    --------
    pd.Series
        The calculated EMA values
    
    Example:
    --------
    If period=10, each EMA value will be calculated using the last 10 periods,
    with more recent periods having more influence on the result.
    """
    return data.ewm(span=period, adjust=False).mean()

def calculate_macd(data: pd.Series, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Tuple[pd.Series, pd.Series]:
    """
    Calculate the Moving Average Convergence Divergence (MACD) indicator.
    
    MACD is a trend-following momentum indicator that shows the relationship
    between two moving averages of a price.
    
    Parameters:
    -----------
    data : pd.Series
        The price series to calculate MACD for (usually closing prices)
    fast_period : int
        The period for the faster EMA (default: 12)
    slow_period : int
        The period for the slower EMA (default: 26)
    signal_period : int
        The period for the signal line EMA (default: 9)
        
    Returns:
    --------
    Tuple[pd.Series, pd.Series]
        A tuple containing:
        1. MACD line (fast EMA - slow EMA)
        2. Signal line (EMA of MACD line)
    
    Example:
    --------
    The MACD line crosses above the signal line → potential buy signal
    The MACD line crosses below the signal line → potential sell signal
    """
    # Calculate the fast and slow EMAs
    fast_ema = calculate_ema(data, fast_period)
    slow_ema = calculate_ema(data, slow_period)
    
    # MACD is the difference between fast and slow EMAs
    macd_line = fast_ema - slow_ema
    
    # Signal line is an EMA of the MACD line
    signal_line = calculate_ema(macd_line, signal_period)
    
    return macd_line, signal_line

def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) indicator.
    
    RSI measures the speed and magnitude of recent price changes to evaluate
    whether a stock is overbought or oversold.
    
    Parameters:
    -----------
    data : pd.Series
        The price series to calculate RSI for (usually closing prices)
    period : int
        The number of periods to use in the RSI calculation (default: 14)
        
    Returns:
    --------
    pd.Series
        The calculated RSI values (0-100)
    
    Interpretation:
    --------------
    - RSI > 70: Potentially overbought
    - RSI < 30: Potentially oversold
    - 50 is considered the centerline
    """
    # Calculate price changes
    delta = data.diff()
    
    # Separate gains (positive) and losses (negative)
    gains = delta.where(delta > 0, 0)  # Keep positive changes, replace negative with 0
    losses = -delta.where(delta < 0, 0)  # Keep negative changes (make positive), replace positive with 0
    
    # Calculate average gains and losses over the specified period
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    # Calculate the Relative Strength (RS)
    rs = avg_gains / avg_losses
    
    # Calculate RSI using the formula: RSI = 100 - (100 / (1 + RS))
    rsi = 100 - (100 / (1 + rs))
    
    return rsi 