# Import required libraries
# abc: for creating abstract base classes (templates for other classes)
# pandas: for data manipulation
# typing: for type hints
# .indicators: our custom indicators module
from abc import ABC, abstractmethod
import pandas as pd
from typing import Tuple
from .indicators import calculate_macd, calculate_ema, calculate_rsi

class Strategy(ABC):
    """
    Abstract base class that defines what a trading strategy should look like.
    
    This is a template that all specific trading strategies must follow.
    It ensures that every strategy implements the required methods.
    
    ABC (Abstract Base Class) means this class is not meant to be used directly,
    but rather to be inherited from by specific strategy classes.
    """
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on the strategy's rules.
        
        This is an abstract method, which means every strategy class that inherits
        from this class MUST implement this method.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Price data with OHLCV columns (Open, High, Low, Close, Volume)
            
        Returns:
        --------
        pd.Series
            A series of trading signals where:
            1 = Buy signal
            -1 = Sell signal
            0 = No action
        """
        pass

class MACDStrategy(Strategy):
    """
    A trading strategy based on MACD (Moving Average Convergence Divergence).
    
    This strategy generates buy signals when the MACD line crosses above its own EMA,
    and sell signals when it crosses below.
    """
    
    def __init__(self, macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9, 
                 ema_period: int = 10):
        """
        Initialize the MACD strategy with customizable parameters.
        
        Parameters:
        -----------
        macd_fast : int
            Period for the fast EMA in MACD calculation (default: 12)
        macd_slow : int
            Period for the slow EMA in MACD calculation (default: 26)
        macd_signal : int
            Period for the MACD signal line (default: 9)
        ema_period : int
            Period for the EMA of the MACD line (default: 10)
        """
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.ema_period = ema_period
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on MACD crosses of its own EMA.
        
        Strategy Rules:
        --------------
        Buy (1) when: MACD line crosses above its EMA
        Sell (-1) when: MACD line crosses below its EMA
        Hold (0) otherwise
        
        Parameters:
        -----------
        data : pd.DataFrame
            Price data with OHLCV columns
            
        Returns:
        --------
        pd.Series
            Trading signals (1, -1, or 0)
        """
        # Calculate MACD (we don't need the signal line for this strategy)
        macd_line, _ = calculate_macd(data['close'], 
                                    self.macd_fast, 
                                    self.macd_slow, 
                                    self.macd_signal)
        
        # Calculate EMA of MACD line
        macd_ema = calculate_ema(macd_line, self.ema_period)
        
        # Generate signals based on MACD crossing its EMA
        signals = pd.Series(0, index=data.index)  # Start with no signals
        signals[macd_line > macd_ema] = 1  # Buy when MACD is above its EMA
        signals[macd_line < macd_ema] = -1  # Sell when MACD is below its EMA
        
        return signals

class RSIEMAStrategy(Strategy):
    """
    A trading strategy combining RSI (Relative Strength Index) with EMA (Exponential Moving Average).
    
    This strategy looks for oversold conditions (RSI < 30) combined with price
    trending above its EMA for buy signals, and overbought conditions (RSI > 70)
    or price below EMA for sell signals.
    """
    
    def __init__(self, rsi_period: int = 14, ema_period: int = 21, 
                 rsi_oversold: float = 30, rsi_overbought: float = 70):
        """
        Initialize the RSI-EMA strategy with customizable parameters.
        
        Parameters:
        -----------
        rsi_period : int
            Period for RSI calculation (default: 14)
        ema_period : int
            Period for EMA calculation (default: 21)
        rsi_oversold : float
            RSI level below which we consider the market oversold (default: 30)
        rsi_overbought : float
            RSI level above which we consider the market overbought (default: 70)
        """
        self.rsi_period = rsi_period
        self.ema_period = ema_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on RSI and EMA conditions.
        
        Strategy Rules:
        --------------
        Buy (1) when: RSI crosses above oversold (30) AND price is above EMA
        Sell (-1) when: RSI crosses above overbought (70) OR price falls below EMA
        Hold (0) otherwise
        
        Parameters:
        -----------
        data : pd.DataFrame
            Price data with OHLCV columns
            
        Returns:
        --------
        pd.Series
            Trading signals (1, -1, or 0)
        """
        # Calculate our technical indicators
        rsi = calculate_rsi(data['close'], self.rsi_period)
        ema = calculate_ema(data['close'], self.ema_period)
        
        # Initialize signal series with zeros (no position)
        signals = pd.Series(0, index=data.index)
        
        # Generate buy signals
        buy_condition = (rsi > self.rsi_oversold) & (data['close'] > ema)
        signals[buy_condition] = 1
        
        # Generate sell signals
        sell_condition = (rsi > self.rsi_overbought) | (data['close'] < ema)
        signals[sell_condition] = -1
        
        return signals 