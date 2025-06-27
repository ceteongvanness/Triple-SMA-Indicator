"""
# Triple SMA Trading Strategy with QuantStats for Google Colab
# Using pandas, numpy, matplotlib, and QuantStats

This notebook implements the Triple SMA (20/50/200) trading strategy
with comprehensive performance analytics using QuantStats.
"""

# Install required packages
!pip install pandas numpy matplotlib
!pip install quantstats

# Install IBKR API
!pip install --upgrade pip
!pip install ibapi

# Verify installation
try:
    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    import quantstats as qs
    print("All required packages successfully installed!")
except ImportError as e:
    print(f"Package installation failed: {e}")

# Import required libraries
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import functools
import quantstats as qs

# Enable QuantStats Jupyter integration
qs.extend_pandas()

# Set matplotlib style for better visualizations
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 7)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # Initialize variable to store candle data
        self.positions = {}  # Dictionary to store current positions
        self.data_received = False
        
    def historicalData(self, reqId, bar):
        # Called when historical data is received
        self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])
        
    def historicalDataEnd(self, reqId, start, end):
        # Called when all historical data has been received
        print(f"Historical data received from {start} to {end}")
        self.data_received = True
        
    def position(self, account, contract, position, avgCost):
        # Called when position information is received
        super().position(account, contract, position, avgCost)
        key = contract.symbol
        self.positions[key] = position
        print(f"Current position for {key}: {position} shares at avg cost of {avgCost}")
        
    def nextValidId(self, orderId):
        # Called when connection is established and next valid order ID is received
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        print(f"Connected to TWS. Next valid order ID: {orderId}")
        
    def error(self, reqId, errorCode, errorString):
        # Called when an error occurs
        print(f"Error {errorCode}: {errorString}")
        
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, 
                   permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        # Called when order status changes
        print(f"Order {orderId} status: {status}, filled: {filled}, remaining: {remaining}, price: {avgFillPrice}")


def create_contract(symbol, secType='STK', exchange='SMART', currency='USD'):
    """Create a contract object for a specific security"""
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract


def create_order(action, quantity, order_type='MKT'):
    """Create an order object"""
    order = Order()
    order.action = action
    order.totalQuantity = quantity
    order.orderType = order_type
    return order


@functools.lru_cache(maxsize=32)
def calculate_triple_sma_optimized(data_tuple, sma20_period=20, sma50_period=50, sma200_period=200):
    """
    Calculate Triple SMA and generate signals based on the strategy using optimized pandas
    
    Note: data_tuple is a tuple representation of the data for caching purposes
    """
    # Convert tuple back to list for processing
    data = list(data_tuple)
    
    # Pre-allocate DataFrame with known size for better performance
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    
    # Convert date strings to datetime objects if needed
    if isinstance(df['date'].iloc[0], str):
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d %H:%M:%S')
    
    # Set date as index for QuantStats compatibility
    df = df.set_index('date')
    
    # Calculate SMAs using pandas rolling - vectorized operation
    df['sma20'] = df['close'].rolling(window=sma20_period).mean()
    df['sma50'] = df['close'].rolling(window=sma50_period).mean()
    df['sma200'] = df['close'].rolling(window=sma200_period).mean()
    
    # Generate signals using vectorized operations instead of loops
    # Create boolean masks for conditions
    uptrend = (df['close'] > df['sma20']) & (df['sma20'] > df['sma50']) & (df['sma50'] > df['sma200'])
    downtrend = (df['close'] < df['sma20']) & (df['sma20'] < df['sma50']) & (df['sma50'] < df['sma200'])
    
    # Initialize signal column with zeros
    df['signal'] = 0
    
    # Apply conditions using vectorized operations
    df.loc[uptrend, 'signal'] = 1
    df.loc[downtrend, 'signal'] = -1
    
    # Calculate position changes using diff (vectorized)
    df['position'] = df['signal'].diff()
    
    # Calculate returns for QuantStats
    df['returns'] = df['close'].pct_change()
    
    # Calculate strategy returns (position at previous day's close * today's return)
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    
    # Fill NaN values with zeros
    df['strategy_returns'] = df['strategy_returns'].fillna(0)
    
    return df


def visualize_triple_sma_strategy_optimized(df, symbol):
    """
    Visualize the Triple SMA strategy results with optimized matplotlib
    """
    # Create a copy of df with date as a column for plotting
    plot_df = df.reset_index()
    
    # Create figure with specific size for better quality
    fig, ax = plt.subplots(figsize=(14, 7), dpi=100)
    
    # Format dates for better display
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    # Plot price and SMAs with optimized Line2D objects for large datasets
    ax.plot(plot_df['date'], plot_df['close'], label='Close Price', alpha=0.7, linewidth=1)
    ax.plot(plot_df['date'], plot_df['sma20'], label='SMA 20', color='#3177e0', linewidth=1.5)
    ax.plot(plot_df['date'], plot_df['sma50'], label='SMA 50', color='#ff9800', linewidth=1.5)
    ax.plot(plot_df['date'], plot_df['sma200'], label='SMA 200', color='#f44336', linewidth=1.5)
    
    # Plot buy/sell signals
    buy_signals = plot_df[plot_df['position'] > 0]
    sell_signals = plot_df[plot_df['position'] < 0]
    
    # Use scatter for signals
    ax.scatter(buy_signals['date'], buy_signals['close'], marker='^', color='green', s=80, label='Buy Signal')
    ax.scatter(sell_signals['date'], sell_signals['close'], marker='v', color='red', s=80, label='Sell Signal')
    
    # Add grid and labels with improved styling
    ax.set_title(f'Triple SMA Strategy for {symbol}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
    
    # Adjust layout to prevent cut-off labels
    plt.tight_layout()
    
    # Show plot
    plt.show()
    
    return fig


def generate_quantstats_reports(df, symbol, benchmark_ticker='SPY'):
    """
    Generate comprehensive performance reports using QuantStats
    """
    print("\n=== Generating QuantStats Reports ===")
    
    # Extract strategy returns for QuantStats
    strategy_returns = df['strategy_returns']
    
    # Basic metrics
    print("\nBasic Performance Metrics:")
    print(f"CAGR: {qs.stats.cagr(strategy_returns):.2%}")
    print(f"Sharpe Ratio: {qs.stats.sharpe(strategy_returns):.2f}")
    print(f"Max Drawdown: {qs.stats.max_drawdown(strategy_returns):.2%}")
    print(f"Win Rate: {qs.stats.win_rate(strategy_returns):.2%}")
    print(f"Volatility (Ann.): {qs.stats.volatility(strategy_returns, annualize=True):.2%}")
    
    # Plot returns
    print("\nPlotting Cumulative Returns...")
    qs.plots.returns(strategy_returns, benchmark=benchmark_ticker, savefig=f'{symbol}_returns.png')
    
    # Plot drawdowns
    print("\nPlotting Drawdowns...")
    qs.plots.drawdown(strategy_returns, savefig=f'{symbol}_drawdowns.png')
    
    # Plot monthly returns heatmap
    print("\nPlotting Monthly Returns Heatmap...")
    qs.plots.monthly_heatmap(strategy_returns, savefig=f'{symbol}_monthly_heatmap.png')
    
    # Generate full tearsheet
    print("\nGenerating Full Tearsheet...")
    try:
        qs.reports.html(strategy_returns, benchmark=benchmark_ticker, 
                        title=f'Triple SMA Strategy - {symbol}',
                        output=f'{symbol}_tearsheet.html')
        print(f"Full tearsheet saved as {symbol}_tearsheet.html")
    except Exception as e:
        print(f"Error generating HTML tearsheet: {e}")
        print("Generating basic metrics report instead...")
        qs.reports.metrics(strategy_returns, benchmark=benchmark_ticker, mode='basic')
    
    return strategy_returns


def test_triple_sma_strategy(host='127.0.0.1', port=7497, symbol='AAPL', benchmark_ticker='SPY'):
    """Test the Triple SMA strategy for a specific symbol using optimized pandas and QuantStats"""
    # Connect to TWS
    app = IBapi()
    app.connect(host, port, 0)  # 7497 for TWS Paper Trading
    
    # Start the socket in a separate thread
    api_thread = threading.Thread(target=app.run, daemon=True)
    api_thread.start()
    
    # Wait for connection to establish
    time.sleep(2)
    
    if not app.isConnected():
        print("Failed to connect to TWS. Please check if TWS is running and API connections are enabled.")
        return None
    
    # Create contract for the symbol
    contract = create_contract(symbol)
    
    # Request historical data
    app.data = []  # Reset data
    app.data_received = False
    
    # Request 2 years of daily data to have enough for SMA 200
    app.reqHistoricalData(
        reqId=1,
        contract=contract,
        endDateTime='',  # Empty string means "now"
        durationStr='2 Y',  # Duration of data (2 years)
        barSizeSetting='1 day',  # Bar size (1 day)
        whatToShow='MIDPOINT',  # Type of data
        useRTH=1,  # Regular Trading Hours only
        formatDate=1,  # Date format (1 = yyyyMMdd HH:mm:ss)
        keepUpToDate=False,  # Don't keep updating
        chartOptions=[]  # No chart options
    )
    
    # Wait for data to be received
    timeout = 15  # seconds
    start_time = time.time()
    while not app.data_received and time.time() - start_time < timeout:
        time.sleep(0.5)
    
    # Disconnect
    app.disconnect()
    
    # Process data and apply strategy
    if len(app.data) > 0:
        print(f"Received {len(app.data)} bars of historical data for {symbol}")
        
        # Start timing for performance measurement
        start_time = time.time()
        
        # Convert data to tuple for caching
        data_tuple = tuple(map(tuple, app.data))
        
        # Calculate Triple SMA and generate signals using optimized pandas
        df = calculate_triple_sma_optimized(data_tuple)
            
        # End timing
        execution_time = time.time() - start_time
        print(f"Strategy calculation took {execution_time:.4f} seconds")
        
        # Visualize the strategy
        visualize_triple_sma_strategy_optimized(df, symbol)
        
        # Calculate performance metrics
        if len(df[df['position'] != 0]) > 0:
            # Count buy and sell signals
            buy_signals = len(df[df['position'] > 0])
            sell_signals = len(df[df['position'] < 0])
            
            print(f"\nStrategy Performance Summary for {symbol}:")
            print(f"Total Buy Signals: {buy_signals}")
            print(f"Total Sell Signals: {sell_signals}")
            
            # Current signal
            current_signal = df['signal'].iloc[-1]
            if current_signal == 1:
                print(f"Current Signal: BUY/HOLD (Strong Uptrend)")
            elif current_signal == -1:
                print(f"Current Signal: SELL/SHORT (Strong Downtrend)")
            else:
                print(f"Current Signal: NEUTRAL (No Clear Trend)")
            
            # Current SMA values
            print(f"\nCurrent SMA Values:")
            print(f"SMA 20: {df['sma20'].iloc[-1]:.2f}")
            print(f"SMA 50: {df['sma50'].iloc[-1]:.2f}")
            print(f"SMA 200: {df['sma200'].iloc[-1]:.2f}")
            print(f"Current Price: {df['close'].iloc[-1]:.2f}")
            
            # Generate QuantStats reports
            generate_quantstats_reports(df, symbol, benchmark_ticker)
            
        else:
            print("No trading signals generated for the given data.")
        
        return df
    else:
        print(f"No data received for {symbol}")
        return None


def execute_trade(host, port, symbol, action, quantity):
    """Execute a trade for a specific symbol"""
    # Connect to TWS
    app = IBapi()
    app.connect(host, port, 0)  # Connect to TWS
    
    # Start the socket in a separate thread
    api_thread = threading.Thread(target=app.run, daemon=True)
    api_thread.start()
    
    # Wait for connection to establish
    time.sleep(2)
    
    if not app.isConnected():
        print("Failed to connect to TWS. Please check if TWS is running and API connections are enabled.")
        return False
    
    # Create contract for the symbol
    contract = create_contract(symbol)
    
    # Create order
    order = create_order(action, quantity)
    
    # Place order
    app.placeOrder(app.nextOrderId, contract, order)
    print(f"Placed {action} order for {quantity} shares of {symbol}")
    
    # Wait for order to be processed
    time.sleep(3)
    
    # Disconnect
    app.disconnect()
    
    return True


def run_with_sample_data(symbol="Sample", benchmark_ticker=None):
    """Run the strategy with sample data and generate QuantStats reports"""
    print("\nUsing sample data for demonstration...")
    
    # Generate sample data
    import numpy as np
    
    # Create dates
    start_date = pd.Timestamp('2023-01-01')
    dates = [start_date + pd.Timedelta(days=i) for i in range(500)]
    
    # Generate price data with some trend and noise
    np.random.seed(42)  # For reproducibility
    price = 100
    prices = [price]
    for _ in range(499):
        change = np.random.normal(0, 1) / 100  # Random daily return
        price = price * (1 + change)
        prices.append(price)
    
    # Create sample data in the format expected by the strategy
    sample_data = []
    for i, date in enumerate(dates):
        sample_data.append([
            date.strftime('%Y%m%d %H:%M:%S'),
            prices[i] * 0.99,  # Open
            prices[i] * 1.01,  # High
            prices[i] * 0.98,  # Low
            prices[i],         # Close
            int(np.random.normal(1000000, 200000))  # Volume
        ])
    
    # Convert to tuple for caching
    sample_data_tuple = tuple(map(tuple, sample_data))
    
    # Calculate Triple SMA and generate signals
    df = calculate_triple_sma_optimized(sample_data_tuple)
    
    # Visualize the strategy
    visualize_triple_sma_strategy_optimized(df, symbol)
    
    # Generate QuantStats reports
    generate_quantstats_reports(df, symbol, benchmark_ticker)
    
    return df


# Main execution section - Run this in Colab

# Ask if using ngrok
use_ngrok = input("Are you using ngrok to connect to TWS/IB Gateway? (y/n): ").lower() == 'y'

if use_ngrok:
    # Get ngrok connection details
    ngrok_host = input("Enter your ngrok host (e.g., 0.tcp.ngrok.io): ")
    ngrok_port = int(input("Enter your ngrok port: "))
    host = ngrok_host
    port = ngrok_port
else:
    # Use default connection (only works if Colab is running locally)
    host = input("Enter TWS/IB Gateway host (default: 127.0.0.1): ") or "127.0.0.1"
    port = int(input("Enter TWS/IB Gateway port (default: 7497 for paper trading): ") or "7497")

print("\n=== Triple SMA Trading Strategy with QuantStats ===")
print("This notebook implements a trading strategy based on 20, 50, and 200-day Simple Moving Averages.")
print("Options:")
print("1. Test the strategy (backtest and visualize with QuantStats)")
print("2. Execute a trade based on current signal")
print("3. Use sample data with QuantStats (no IBKR connection needed)")

choice = input("Enter your choice (1-3): ")

if choice == "1":
    # Test the strategy
    symbol = input("Enter symbol to test (default: AAPL): ") or "AAPL"
    benchmark = input("Enter benchmark ticker (default: SPY): ") or "SPY"
    
    print(f"\nTesting Triple SMA strategy for {symbol} with {benchmark} benchmark...")
    test_triple_sma_strategy(host, port, symbol, benchmark)
    
elif choice == "2":
    # Execute a trade
    symbol = input("Enter symbol to trade (default: AAPL): ") or "AAPL"
    action = input("Enter action (BUY or SELL): ").upper()
    quantity = int(input("Enter quantity: "))
    
    if action in ["BUY", "SELL"]:
        print(f"\nExecuting {action} order for {quantity} shares of {symbol}...")
        success = execute_trade(host, port, symbol, action, quantity)
        if success:
            print(f"Order for {symbol} successfully submitted.")
        else:
            print(f"Failed to submit order for {symbol}.")
    else:
        print("Invalid action. Must be BUY or SELL.")

elif choice == "3":
    # Use sample data
    symbol_name = input("Enter a name for your sample data (default: SAMPLE): ") or "SAMPLE"
    benchmark = input("Enter benchmark ticker for comparison (optional, press Enter to skip): ")
    
    run_with_sample_data(symbol_name, benchmark)
    
else:
    print("Invalid choice.")
