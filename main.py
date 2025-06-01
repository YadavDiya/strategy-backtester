# Import our custom modules
from src.data_fetcher import BinanceDataFetcher
from src.strategies import MACDStrategy, RSIEMAStrategy
from src.backtester import Backtester
import pandas as pd
from datetime import datetime
import os

def create_output_directory():
    """
    Create a directory for storing backtester outputs.
    Directory name format: backtester_output_YYYY_MM_DD
    """
    # Get current date
    current_date = datetime.now().strftime("%Y_%m_%d")
    # Create directory name
    output_dir = f"backtester_output_{current_date}"
    
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return output_dir

def format_trades_dataframe(df):
    """
    Format the trades DataFrame for better Excel output
    """
    # Ensure columns are in the correct order
    columns = [
        "Entry Time", "Entry Price", "Exit Time", "Exit Price",
        "Strategy", "PnL", "Status"
    ]
    df = df[columns]
    
    # Format numeric columns
    df["Entry Price"] = df["Entry Price"].round(2)
    df["Exit Price"] = df["Exit Price"].round(2)
    df["PnL"] = df["PnL"].round(2)
    
    return df

def main():
    """
    Main function that runs our backtesting system.
    
    This function:
    1. Downloads historical price data from Binance
    2. Sets up our trading strategies
    3. Runs backtests for each strategy
    4. Displays and saves the results in Excel format
    """
    # Create output directory
    output_dir = create_output_directory()
    
    # Create a data fetcher object to download price data
    print("Initializing data fetcher...")
    fetcher = BinanceDataFetcher()
    
    # Download the latest data for Bitcoin/USDT
    print("\nDownloading price data...")
    symbol = "BTCUSDT"  # Bitcoin quoted in USDT
    data = fetcher.fetch_klines(symbol)
    print(f"Successfully loaded {len(data)} candles for {symbol}")
    
    # Create instances of our trading strategies
    print("\nInitializing trading strategies...")
    macd_strategy = MACDStrategy()  # MACD crossover strategy
    rsi_strategy = RSIEMAStrategy()  # RSI with EMA strategy
    
    # List of strategies to test
    strategies = [
        ("MACD Strategy", macd_strategy),
        ("RSI-EMA Strategy", rsi_strategy)
    ]
    
    # Store results from all strategies
    results = []
    
    # Run backtest for each strategy
    for strategy_name, strategy in strategies:
        print(f"\nRunning backtest for {strategy_name}")
        
        # Create and run backtester for this strategy
        backtester = Backtester(data, strategy)
        trades_df = backtester.run()
        
        # Get performance metrics for this strategy
        metrics = backtester.get_performance_metrics()
        
        # Display the results
        print("\nPerformance Metrics:")
        for metric, value in metrics.items():
            if metric in ["Win Rate", "Average PnL"]:
                print(f"{metric}: {value:.2f}%")
            else:
                print(f"{metric}: {value:.2f}")
        
        # Store the results
        results.append(trades_df)
    
    # If we have any results, combine them and save to Excel
    if results:
        # Combine results from all strategies
        all_trades = pd.concat(results, ignore_index=True)
        
        # Format the DataFrame
        all_trades = format_trades_dataframe(all_trades)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backtester_results_{timestamp}.xlsx"
        filepath = os.path.join(output_dir, filename)
        
        # Save to Excel with proper formatting
        print(f"\nSaving trades to Excel...")
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            all_trades.to_excel(writer, index=False, sheet_name='Trades')
            
            # Auto-adjust columns width
            worksheet = writer.sheets['Trades']
            for idx, col in enumerate(all_trades.columns):
                max_length = max(
                    all_trades[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length
        
        print(f"Results saved to {filepath}")
        
        # Also save summary metrics
        summary_df = pd.DataFrame([metrics])
        summary_filepath = os.path.join(output_dir, f"summary_metrics_{timestamp}.xlsx")
        summary_df.to_excel(summary_filepath, index=False)
        print(f"Summary metrics saved to {summary_filepath}")

# This is the standard Python idiom for running the main function
# It only runs if this file is run directly (not when imported as a module)
if __name__ == "__main__":
    main() 