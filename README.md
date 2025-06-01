# Strategy Backtester v1.0

A powerful Python-based cryptocurrency trading strategy backtester that allows you to test and evaluate trading strategies using historical data from Binance.

## Features

- Real-time data fetching from Binance
- Multiple pre-built trading strategies:
  - MACD Strategy (MACD line crossing its EMA)
  - RSI-EMA Strategy (RSI with EMA trend confirmation)
- Detailed performance metrics and analysis
- Excel-formatted reports with comprehensive trade history
- Easy strategy customization and extension

## Quick Start

1. Clone the repository:
```bash
git clone [repository-url]
cd strategy-backtester
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backtester:
```bash
python main.py
```

## Project Structure

- `src/`
  - `data_fetcher.py`: Handles data retrieval from Binance
  - `indicators.py`: Technical indicator implementations
  - `strategies.py`: Trading strategy implementations
  - `backtester.py`: Core backtesting engine
- `main.py`: Main execution script
- `docs/`: Documentation directory
  - `User Manual.docx`: Comprehensive user guide
- `requirements.txt`: Project dependencies

## Output

The backtester generates two types of output files in a dated directory (`backtester_output_YYYY_MM_DD/`):

1. Trade Results (`backtester_results_YYYYMMDD_HHMMSS.xlsx`)
   - Detailed trade history
   - Entry/Exit points
   - PnL calculations

2. Summary Metrics (`summary_metrics_YYYYMMDD_HHMMSS.xlsx`)
   - Overall performance statistics
   - Win rate
   - Total and average PnL

## Documentation

For detailed information about installation, usage, and customization, please refer to the [User Manual](docs/User Manual.docx) in the docs directory.

## Version History

### v1.0 (Initial Release)
- Complete backtesting system implementation
- Two trading strategies (MACD and RSI-EMA)
- Excel-formatted output with detailed analytics
- Comprehensive documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details. 