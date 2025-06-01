# Import required libraries
# pandas: for data manipulation
# typing: for type hints
# datetime: for working with dates and times
# .strategies: our custom Strategy class
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from .strategies import Strategy

class Trade:
    """
    A class that represents a single trade with its entry and exit details.
    
    This class keeps track of:
    - When we entered the trade
    - At what price we entered
    - When we exited (if we have)
    - At what price we exited
    - How much profit or loss we made
    - Whether the trade was successful
    """
    
    def __init__(self, entry_time: datetime, entry_price: float, strategy_name: str):
        """
        Initialize a new trade.
        
        Parameters:
        -----------
        entry_time : datetime
            When we entered the trade
        entry_price : float
            The price at which we entered
        strategy_name : str
            Name of the strategy that generated this trade
        """
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.exit_time = None  # Will be set when we exit the trade
        self.exit_price = None  # Will be set when we exit the trade
        self.pnl = 0.0  # Profit/Loss (will be calculated when we exit)
        self.status = "OPEN"  # Current status of the trade
        self.strategy_name = strategy_name
    
    def close_trade(self, exit_time: datetime, exit_price: float, position_size: float = 1.0):
        """
        Close an open trade and calculate its profit or loss.
        
        Parameters:
        -----------
        exit_time : datetime
            When we exited the trade
        exit_price : float
            The price at which we exited
        position_size : float
            How many units we traded (default: 1.0)
        """
        self.exit_time = exit_time
        self.exit_price = exit_price
        # Calculate profit/loss: (exit price - entry price) * how many units we traded
        self.pnl = (self.exit_price - self.entry_price) * position_size
        # Mark the trade as a win or loss
        self.status = "WIN" if self.pnl > 0 else "LOSS"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the trade information to a dictionary format.
        This makes it easy to create a DataFrame of trades later.
        
        Returns:
        --------
        Dict[str, Any]
            Dictionary containing all trade information
        """
        return {
            "Entry Time": self.entry_time,
            "Entry Price": self.entry_price,
            "Exit Time": self.exit_time,
            "Exit Price": self.exit_price,
            "Strategy": self.strategy_name,
            "PnL": self.pnl,
            "Status": self.status
        }

class Backtester:
    """
    The main backtesting engine that simulates trading based on strategy signals.
    
    This class:
    1. Takes a trading strategy and historical price data
    2. Simulates trading based on the strategy's signals
    3. Keeps track of all trades and their performance
    4. Calculates overall performance metrics
    """
    
    def __init__(self, data: pd.DataFrame, strategy: Strategy, position_size: float = 1.0):
        """
        Initialize the backtester.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Historical price data (OHLCV)
        strategy : Strategy
            The trading strategy to test
        position_size : float
            How many units to trade each time (default: 1.0)
        """
        self.data = data
        self.strategy = strategy
        self.position_size = position_size
        self.trades: List[Trade] = []  # List to store all completed trades
        self.current_trade = None  # The currently open trade (if any)
    
    def run(self) -> pd.DataFrame:
        """
        Run the backtest simulation.
        
        This method:
        1. Gets trading signals from the strategy
        2. Simulates entering and exiting trades based on these signals
        3. Keeps track of all trades and their results
        
        Returns:
        --------
        pd.DataFrame
            A DataFrame containing all trades and their results
        """
        # Get trading signals from our strategy
        signals = self.strategy.generate_signals(self.data)
        
        # Go through the data day by day (or candle by candle)
        for timestamp, row in self.data.iterrows():
            signal = signals[timestamp]
            
            # Handle buy signals - enter a new trade if we're not already in one
            if signal == 1 and self.current_trade is None:
                self.current_trade = Trade(
                    entry_time=timestamp,
                    entry_price=row['close'],
                    strategy_name=self.strategy.__class__.__name__
                )
            
            # Handle sell signals - close the current trade if we have one
            elif signal == -1 and self.current_trade is not None:
                self.current_trade.close_trade(
                    exit_time=timestamp,
                    exit_price=row['close'],
                    position_size=self.position_size
                )
                self.trades.append(self.current_trade)
                self.current_trade = None
        
        # If we still have an open trade at the end, close it at the last price
        if self.current_trade is not None:
            last_timestamp = self.data.index[-1]
            last_price = self.data['close'].iloc[-1]
            self.current_trade.close_trade(
                exit_time=last_timestamp,
                exit_price=last_price,
                position_size=self.position_size
            )
            self.trades.append(self.current_trade)
        
        # Convert all trades to a DataFrame for easy analysis
        trades_df = pd.DataFrame([trade.to_dict() for trade in self.trades])
        
        return trades_df
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Calculate various performance metrics for our trading strategy.
        
        Returns:
        --------
        Dict[str, float]
            Dictionary containing:
            - Total number of trades
            - Win rate (percentage of profitable trades)
            - Total profit/loss
            - Average profit/loss per trade
        """
        # If we haven't made any trades, return zeros
        if not self.trades:
            return {
                "Total Trades": 0,
                "Win Rate": 0.0,
                "Total PnL": 0.0,
                "Average PnL": 0.0
            }
        
        # Calculate metrics
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t.pnl > 0])
        total_pnl = sum(t.pnl for t in self.trades)
        
        return {
            "Total Trades": total_trades,
            "Win Rate": (winning_trades / total_trades) * 100,  # Convert to percentage
            "Total PnL": total_pnl,
            "Average PnL": total_pnl / total_trades
        } 