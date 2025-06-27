# ============================================================================
# ENHANCED COLAB NOTEBOOK WITH ROBUST NGROK/IBKR INTEGRATION
# ============================================================================

# ============================================================================
# CELL 1: Install Required Packages (Enhanced)
# ============================================================================

"""
Enhanced Triple SMA Trading Strategy with QuantStats for Google Colab
====================================================================

IMPROVEMENTS:
- Robust ngrok connection testing and validation
- Enhanced error handling and retry mechanisms
- Connection status monitoring and auto-reconnection
- Better user interface with progress indicators
- Comprehensive logging and debugging features
- Market data validation and quality checks

Run each cell sequentially for best results.
"""

print("📦 Installing enhanced package set...")

# Core packages with specific versions for stability
!pip install pandas>=1.5.0 numpy>=1.21.0 matplotlib>=3.6.0

# IBKR API with latest version
!pip install --upgrade pip
!pip install ibapi>=10.19.1

# Performance analytics with latest features
!pip install quantstats>=0.0.62

# Additional utilities for enhanced functionality
!pip install yfinance>=0.2.10
!pip install requests>=2.28.0  # For ngrok API checking
!pip install tabulate>=0.9.0   # For better table formatting

print("✅ Enhanced package set installed successfully!")

# ============================================================================
# CELL 2: Enhanced Imports and Configuration
# ============================================================================

# Enhanced imports with error handling
try:
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
    import requests
    import socket
    import json
    from tabulate import tabulate
    import warnings
    
    print("✅ All enhanced packages imported successfully!")
    
except ImportError as e:
    print(f"❌ Package import failed: {e}")
    print("Please run the installation cell above and try again.")

# Enhanced configuration
warnings.filterwarnings('ignore')  # Suppress warnings for cleaner output
qs.extend_pandas()

# Enhanced matplotlib configuration
plt.style.use('default')
plt.rcParams['figure.figsize'] = (15, 8)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['font.size'] = 10

print("🎨 Enhanced matplotlib styling configured")
print("📊 QuantStats integration enabled with warnings suppressed")

# ============================================================================
# CELL 3: Enhanced Connection Management System
# ============================================================================

class ConnectionManager:
    """Enhanced connection manager for ngrok and IBKR"""
    
    def __init__(self):
        self.ngrok_status = None
        self.ibkr_status = None
        self.last_successful_connection = None
        self.connection_history = []
    
    def check_ngrok_status(self):
        """Check ngrok tunnel status via local API"""
        try:
            response = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=5)
            
            if response.status_code == 200:
                tunnels = response.json()
                if tunnels['tunnels']:
                    self.ngrok_status = "active"
                    tunnel_info = []
                    for tunnel in tunnels['tunnels']:
                        public_url = tunnel['public_url']
                        config = tunnel['config']
                        tunnel_info.append({
                            'public_url': public_url,
                            'local_addr': config['addr'],
                            'proto': tunnel['proto']
                        })
                    return True, tunnel_info
                else:
                    self.ngrok_status = "no_tunnels"
                    return False, "ngrok running but no tunnels found"
            else:
                self.ngrok_status = "error"
                return False, f"ngrok API returned status: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            self.ngrok_status = "not_running"
            return False, "ngrok not running or not accessible on port 4040"
        except Exception as e:
            self.ngrok_status = "error"
            return False, f"Error checking ngrok: {e}"
    
    def test_network_connection(self, host, port, timeout=10):
        """Enhanced network connectivity test"""
        try:
            start_time = time.time()
            sock = socket.create_connection((host, port), timeout=timeout)
            connection_time = time.time() - start_time
            sock.close()
            
            self.connection_history.append({
                'timestamp': datetime.datetime.now(),
                'host': host,
                'port': port,
                'status': 'success',
                'latency': connection_time
            })
            
            return True, f"Connected in {connection_time:.3f}s"
            
        except socket.gaierror as e:
            error_msg = f"DNS resolution failed: {e}"
            self.connection_history.append({
                'timestamp': datetime.datetime.now(),
                'host': host,
                'port': port,
                'status': 'dns_error',
                'error': str(e)
            })
            return False, error_msg
            
        except socket.timeout:
            error_msg = f"Connection timeout after {timeout}s"
            self.connection_history.append({
                'timestamp': datetime.datetime.now(),
                'host': host,
                'port': port,
                'status': 'timeout',
                'error': error_msg
            })
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Connection failed: {e}"
            self.connection_history.append({
                'timestamp': datetime.datetime.now(),
                'host': host,
                'port': port,
                'status': 'error',
                'error': str(e)
            })
            return False, error_msg
    
    def get_connection_stats(self):
        """Get connection statistics"""
        if not self.connection_history:
            return "No connection attempts recorded"
        
        total_attempts = len(self.connection_history)
        successful = len([c for c in self.connection_history if c['status'] == 'success'])
        success_rate = (successful / total_attempts) * 100
        
        if successful > 0:
            avg_latency = np.mean([c.get('latency', 0) for c in self.connection_history if c['status'] == 'success'])
            return f"Success rate: {success_rate:.1f}% ({successful}/{total_attempts}), Avg latency: {avg_latency:.3f}s"
        else:
            return f"Success rate: 0% (0/{total_attempts})"

# Global connection manager instance
conn_mgr = ConnectionManager()

print("🔗 Enhanced connection management system initialized")

# ============================================================================
# CELL 4: Enhanced IBKR API Wrapper with Robust Error Handling
# ============================================================================

class EnhancedIBapi(EWrapper, EClient):
    """Enhanced IBKR API wrapper with robust error handling and monitoring"""
    
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        self.positions = {}
        self.data_received = False
        self.connection_status = "disconnected"
        self.last_error = None
        self.data_quality_issues = []
        self.connection_time = None
        self.managed_accounts = []
        self.market_data_status = {}
        
    def connectAck(self):
        """Enhanced connection acknowledgment"""
        super().connectAck()
        self.connection_status = "acknowledged"
        print("✅ TWS connection acknowledged")
        
    def nextValidId(self, orderId):
        """Enhanced next valid ID with connection timing"""
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        self.connection_status = "connected"
        self.connection_time = time.time()
        conn_mgr.last_successful_connection = datetime.datetime.now()
        print(f"🔗 TWS fully connected! Next valid order ID: {orderId}")
        
    def managedAccounts(self, accountsList):
        """Enhanced managed accounts handling"""
        super().managedAccounts(accountsList)
        self.managed_accounts = accountsList.split(',') if accountsList else []
        print(f"💼 Managed accounts: {accountsList}")
        
    def historicalData(self, reqId, bar):
        """Enhanced historical data with quality validation"""
        # Validate data quality
        if bar.open <= 0 or bar.high <= 0 or bar.low <= 0 or bar.close <= 0:
            self.data_quality_issues.append(f"Invalid price data on {bar.date}")
            return
            
        if bar.high < bar.low:
            self.data_quality_issues.append(f"High < Low on {bar.date}")
            return
            
        if bar.close > bar.high or bar.close < bar.low:
            self.data_quality_issues.append(f"Close outside High/Low range on {bar.date}")
            return
            
        self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])
        
    def historicalDataEnd(self, reqId, start, end):
        """Enhanced historical data end with quality report"""
        super().historicalDataEnd(reqId, start, end)
        self.data_received = True
        
        print(f"📈 Historical data received: {len(self.data)} bars from {start} to {end}")
        
        if self.data_quality_issues:
            print(f"⚠️ Data quality issues found: {len(self.data_quality_issues)}")
            for issue in self.data_quality_issues[:5]:  # Show first 5 issues
                print(f"   • {issue}")
            if len(self.data_quality_issues) > 5:
                print(f"   • ... and {len(self.data_quality_issues) - 5} more issues")
        else:
            print("✅ Data quality validation passed")
            
    def error(self, reqId, errorCode, errorString):
        """Enhanced error handling with categorization"""
        self.last_error = (errorCode, errorString)
        
        # Categorize errors
        if errorCode in [2104, 2106, 2158]:  # Market data farm connections
            self.market_data_status[errorCode] = errorString
            print(f"✅ Market data: {errorString}")
        elif errorCode in [2137, 2138]:  # Market data warnings
            print(f"⚠️ Market data warning {errorCode}: {errorString}")
        elif errorCode in [502, 503, 504]:  # Connection errors
            self.connection_status = "error"
            print(f"❌ Connection error {errorCode}: {errorString}")
        elif errorCode == 162:  # Historical market data error
            print(f"❌ Historical data error: {errorString}")
        elif errorCode == 200:  # No security definition found
            print(f"❌ Security not found: {errorString}")
        elif errorCode >= 1100 and errorCode <= 1102:  # Connectivity issues
            print(f"⚠️ Connectivity issue {errorCode}: {errorString}")
        else:
            print(f"ℹ️ Message {errorCode}: {errorString}")
            
    def connectionClosed(self):
        """Enhanced connection closed handling"""
        super().connectionClosed()
        self.connection_status = "disconnected"
        print("⚠️ TWS connection closed")
        
    def get_connection_summary(self):
        """Get comprehensive connection summary"""
        summary = {
            'status': self.connection_status,
            'accounts': len(self.managed_accounts),
            'data_bars': len(self.data),
            'data_quality_issues': len(self.data_quality_issues),
            'market_data_farms': len(self.market_data_status),
            'connection_time': self.connection_time
        }
        return summary

print("✅ Enhanced IBKR API wrapper defined with robust error handling")

# ============================================================================
# CELL 5: Enhanced Connection Testing and Validation
# ============================================================================

def comprehensive_connection_test(host=None, port=None, auto_detect=True):
    """Comprehensive connection testing with auto-detection and validation"""
    
    print("🔍 COMPREHENSIVE CONNECTION TEST")
    print("=" * 60)
    
    # Step 1: Check ngrok status
    print("\n1️⃣ Checking ngrok tunnel status...")
    ngrok_ok, ngrok_info = conn_mgr.check_ngrok_status()
    
    if ngrok_ok:
        print("✅ ngrok tunnels detected:")
        for tunnel in ngrok_info:
            if tunnel['proto'] == 'tcp':
                print(f"   📡 {tunnel['public_url']} → {tunnel['local_addr']}")
                if auto_detect and not host:
                    # Auto-extract host and port from ngrok
                    url_parts = tunnel['public_url'].replace('tcp://', '').split(':')
                    if len(url_parts) == 2:
                        host, port = url_parts[0], int(url_parts[1])
                        print(f"   🎯 Auto-detected: {host}:{port}")
    else:
        print(f"⚠️ ngrok issue: {ngrok_info}")
        if auto_detect:
            print("   💡 Make sure ngrok is running: ngrok tcp 7497")
    
    # Get connection details if not auto-detected
    if not host or not port:
        print(f"\n📝 Enter connection details:")
        host = input("🔗 Host (e.g., 0.tcp.ngrok.io): ").strip()
        try:
            port = int(input("🚪 Port (e.g., 12345): ").strip())
        except ValueError:
            print("❌ Invalid port number")
            return False, None, None
    
    print(f"\n2️⃣ Testing network connectivity to {host}:{port}...")
    
    # Multiple connection tests for reliability
    test_results = []
    for i in range(3):
        net_ok, net_msg = conn_mgr.test_network_connection(host, port, timeout=8)
        test_results.append(net_ok)
        if i == 0:  # Show detailed result for first test
            print(f"   Test {i+1}: {'✅' if net_ok else '❌'} {net_msg}")
        else:
            print(f"   Test {i+1}: {'✅' if net_ok else '❌'}")
        
        if not net_ok:
            time.sleep(1)  # Brief pause between failed attempts
    
    success_rate = sum(test_results) / len(test_results)
    if success_rate < 0.7:
        print(f"❌ Network connectivity unreliable ({success_rate:.0%} success rate)")
        return False, host, port
    
    print(f"\n3️⃣ Testing IBKR API connection...")
    
    # Enhanced IBKR API test
    app = EnhancedIBapi()
    
    try:
        app.connect(host, port, clientId=999)
        api_thread = threading.Thread(target=app.run, daemon=True)
        api_thread.start()
        
        # Progressive timeout with status updates
        timeout = 15
        start_time = time.time()
        
        while app.connection_status not in ["connected", "error"] and time.time() - start_time < timeout:
            elapsed = time.time() - start_time
            if elapsed > 5 and elapsed < 6:
                print(f"   ⏳ Still connecting... ({elapsed:.0f}s)")
            elif elapsed > 10 and elapsed < 11:
                print(f"   ⏳ Taking longer than usual... ({elapsed:.0f}s)")
            time.sleep(0.5)
        
        if app.connection_status == "connected":
            connection_summary = app.get_connection_summary()
            print(f"   ✅ IBKR API connected successfully!")
            print(f"   📊 Connection summary:")
            print(f"      • Status: {connection_summary['status']}")
            print(f"      • Accounts: {connection_summary['accounts']}")
            print(f"      • Market data farms: {connection_summary['market_data_farms']}")
            
            app.disconnect()
            
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"   🔗 Validated connection: {host}:{port}")
            print(f"   📊 {conn_mgr.get_connection_stats()}")
            
            return True, host, port
            
        else:
            print(f"   ❌ IBKR API connection failed")
            print(f"   📊 Final status: {app.connection_status}")
            if app.last_error:
                print(f"   ⚠️ Last error: {app.last_error[0]} - {app.last_error[1]}")
            
            app.disconnect()
            return False, host, port
            
    except Exception as e:
        print(f"   ❌ Connection test exception: {e}")
        try:
            app.disconnect()
        except:
            pass
        return False, host, port

def guided_connection_setup():
    """Guided setup process for new users"""
    
    print("🚀 GUIDED CONNECTION SETUP")
    print("=" * 40)
    
    print("\nThis will help you set up the connection to IBKR step by step.")
    print("\n📋 Prerequisites checklist:")
    
    checklist_items = [
        "IBKR paper trading account created and funded",
        "TWS or IB Gateway installed on your LOCAL computer",
        "Logged into TWS with paper trading credentials",
        "API enabled in TWS (File → Global Configuration → API)",
        "Socket port set to 7497 for paper trading",
        "ngrok installed and authenticated on your LOCAL computer",
        "ngrok tunnel running: 'ngrok tcp 7497'"
    ]
    
    print("\n" + "\n".join([f"  □ {item}" for item in checklist_items]))
    
    ready = input(f"\n✅ All items checked? Ready to test connection? (y/n): ").lower().strip()
    
    if ready == 'y':
        success, host, port = comprehensive_connection_test(auto_detect=True)
        
        if success:
            print(f"\n🎯 SETUP COMPLETE!")
            print(f"   Use these settings in your trading code:")
            print(f"   host = '{host}'")
            print(f"   port = {port}")
            return host, port
        else:
            print(f"\n❌ Setup incomplete. Please check the prerequisites and try again.")
            return None, None
    else:
        print(f"\n💡 Please complete the prerequisites checklist and run this again.")
        return None, None

print("🔍 Enhanced connection testing and validation system ready")

# ============================================================================
# CELL 6: Enhanced Strategy Calculation with Data Validation
# ============================================================================

@functools.lru_cache(maxsize=32)
def calculate_triple_sma_enhanced(data_tuple, sma20_period=20, sma50_period=50, sma200_period=200):
    """Enhanced Triple SMA calculation with comprehensive data validation"""
    
    # Convert tuple back to list for processing
    data = list(data_tuple)
    
    if len(data) < sma200_period:
        raise ValueError(f"Insufficient data: {len(data)} bars, need at least {sma200_period}")
    
    # Create DataFrame with enhanced validation
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    
    # Data validation
    original_rows = len(df)
    
    # Remove rows with invalid prices
    df = df[(df['open'] > 0) & (df['high'] > 0) & (df['low'] > 0) & (df['close'] > 0)]
    df = df[df['high'] >= df['low']]
    df = df[(df['close'] <= df['high']) & (df['close'] >= df['low'])]
    
    if len(df) < original_rows:
        print(f"⚠️ Removed {original_rows - len(df)} invalid price bars")
    
    # Convert date strings to datetime objects
    if isinstance(df['date'].iloc[0], str):
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d %H:%M:%S')
    
    # Set date as index and sort
    df = df.set_index('date').sort_index()
    
    # Check for gaps in data
    date_diff = df.index.to_series().diff()
    large_gaps = date_diff[date_diff > pd.Timedelta(days=5)]
    if not large_gaps.empty:
        print(f"⚠️ Found {len(large_gaps)} large gaps in data (>5 days)")
    
    # Calculate SMAs with enhanced error handling
    try:
        df['sma20'] = df['close'].rolling(window=sma20_period, min_periods=sma20_period).mean()
        df['sma50'] = df['close'].rolling(window=sma50_period, min_periods=sma50_period).mean()
        df['sma200'] = df['close'].rolling(window=sma200_period, min_periods=sma200_period).mean()
    except Exception as e:
        raise ValueError(f"Error calculating SMAs: {e}")
    
    # Enhanced signal generation with additional validation
    uptrend = (df['close'] > df['sma20']) & (df['sma20'] > df['sma50']) & (df['sma50'] > df['sma200'])
    downtrend = (df['close'] < df['sma20']) & (df['sma20'] < df['sma50']) & (df['sma50'] < df['sma200'])
    
    # Initialize signals
    df['signal'] = 0
    df.loc[uptrend, 'signal'] = 1
    df.loc[downtrend, 'signal'] = -1
    
    # Calculate position changes and returns
    df['position'] = df['signal'].diff()
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    df['strategy_returns'] = df['strategy_returns'].fillna(0)
    
    # Add volatility and momentum indicators
    df['volatility'] = df['returns'].rolling(window=20).std()
    df['momentum'] = df['close'] / df['close'].shift(10) - 1
    
    # Calculate drawdown
    cumulative_returns = (1 + df['strategy_returns']).cumprod()
    df['drawdown'] = (cumulative_returns / cumulative_returns.expanding().max() - 1)
    
    # Data quality metrics
    valid_sma_data = df.dropna(subset=['sma20', 'sma50', 'sma200'])
    quality_score = len(valid_sma_data) / len(df) * 100
    
    print(f"📊 Data quality score: {quality_score:.1f}%")
    print(f"📈 Valid data range: {valid_sma_data.index[0].date()} to {valid_sma_data.index[-1].date()}")
    
    return df

print("🧮 Enhanced strategy calculation with data validation ready")

# ============================================================================
# CELL 7: Enhanced Visualization with Interactive Features
# ============================================================================

def create_enhanced_visualization(df, symbol):
    """Create enhanced visualization with multiple subplots and indicators"""
    
    # Create subplot layout
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), 
                                        gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # Reset index for plotting
    plot_df = df.reset_index()
    
    # Main price chart with SMAs
    ax1.plot(plot_df['date'], plot_df['close'], label='Close Price', color='black', linewidth=1.5, alpha=0.8)
    ax1.plot(plot_df['date'], plot_df['sma20'], label='SMA 20', color='#3177e0', linewidth=2)
    ax1.plot(plot_df['date'], plot_df['sma50'], label='SMA 50', color='#ff9800', linewidth=2)
    ax1.plot(plot_df['date'], plot_df['sma200'], label='SMA 200', color='#f44336', linewidth=2)
    
    # Add buy/sell signals
    buy_signals = plot_df[plot_df['position'] > 0]
    sell_signals = plot_df[plot_df['position'] < 0]
    
    if not buy_signals.empty:
        ax1.scatter(buy_signals['date'], buy_signals['close'], marker='^', 
                   color='green', s=100, label='Buy Signal', zorder=5, alpha=0.8)
    
    if not sell_signals.empty:
        ax1.scatter(sell_signals['date'], sell_signals['close'], marker='v', 
                   color='red', s=100, label='Sell Signal', zorder=5, alpha=0.8)
    
    # Enhance main chart
    ax1.set_title(f'📊 Enhanced Triple SMA Strategy - {symbol}', fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
    ax1.grid(True, alpha=0.3)
    
    # Format x-axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    
    # Strategy returns chart
    cumulative_returns = (1 + df['strategy_returns']).cumprod()
    ax2.plot(plot_df['date'], cumulative_returns, color='green', linewidth=2, label='Strategy Returns')
    ax2.fill_between(plot_df['date'], 1, cumulative_returns, alpha=0.3, color='green')
    ax2.axhline(y=1, color='black', linestyle='--', alpha=0.5)
    ax2.set_ylabel('Cumulative\nReturns', fontsize=10)
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # Drawdown chart
    ax3.fill_between(plot_df['date'], 0, df['drawdown'] * 100, color='red', alpha=0.3, label='Drawdown')
    ax3.plot(plot_df['date'], df['drawdown'] * 100, color='red', linewidth=1)
    ax3.set_ylabel('Drawdown\n(%)', fontsize=10)
    ax3.set_xlabel('Date', fontsize=12)
    ax3.legend(loc='lower left')
    ax3.grid(True, alpha=0.3)
    
    # Format all x-axes
    for ax in [ax2, ax3]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    
    # Rotate x-axis labels
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()
    
    # Print key statistics
    print(f"\n📊 Enhanced Strategy Statistics:")
    print(f"   📈 Total Return: {(cumulative_returns.iloc[-1] - 1) * 100:.2f}%")
    print(f"   📉 Max Drawdown: {df['drawdown'].min() * 100:.2f}%")
    print(f"   🎯 Number of Trades: {len(buy_signals) + len(sell_signals)}")
    print(f"   📊 Win Rate: {len(df[df['strategy_returns'] > 0]) / len(df[df['strategy_returns'] != 0]) * 100:.1f}%")
    
    return fig

print("📈 Enhanced visualization system with interactive features ready")

# ============================================================================
# CELL 8: Enhanced Main Execution System
# ============================================================================

def enhanced_triple_sma_system():
    """Enhanced main execution system with robust connection management"""
    
    print("🚀 ENHANCED TRIPLE SMA TRADING SYSTEM")
    print("=" * 70)
    print("🔗 Features: Robust ngrok/IBKR integration, Enhanced analytics, Auto-connection")
    print("📊 Strategy: Triple SMA (20/50/200) with QuantStats integration")
    
    print("\n📋 Available Options:")
    print("1️⃣  Guided setup (recommended for first-time users)")
    print("2️⃣  Quick test with auto-detection")
    print("3️⃣  Manual connection test")
    print("4️⃣  Run strategy with real IBKR data")
    print("5️⃣  Demo with sample data")
    print("6️⃣  Connection diagnostics")
    print("7️⃣  System information")
    
    choice = input("\n🎯 Enter your choice (1-7): ").strip()
    
    if choice == "1":
        # Guided setup
        host, port = guided_connection_setup()
        if host and port:
            symbol = input("📈 Enter symbol to analyze (default: AAPL): ").strip().upper() or "AAPL"
            run_enhanced_strategy(host, port, symbol)
        
    elif choice == "2":
        # Quick test with auto-detection
        success, host, port = comprehensive_connection_test(auto_detect=True)
        if success:
            symbol = input("📈 Enter symbol to analyze (default: AAPL): ").strip().upper() or "AAPL"
            run_enhanced_strategy(host, port, symbol)
        
    elif choice == "3":
        # Manual connection test
        success, host, port = comprehensive_connection_test(auto_detect=False)
        if success:
            symbol = input("📈 Enter symbol to analyze (default: AAPL): ").strip().upper() or "AAPL"
            run_enhanced_strategy(host, port, symbol)
        
        elif choice == "4":
        # Run strategy with manual input
        host = input("🔗 Enter host: ").strip()
        try:
            port = int(input("🚪 Enter port: ").strip())
            symbol = input("📈 Enter symbol (default: AAPL): ").strip().upper() or "AAPL"
            run_enhanced_strategy(host, port, symbol)
        except ValueError:
            print("❌ Invalid port number")
        
    elif choice == "5":
        # Demo with sample data
        symbol_name = input("📊 Enter sample name (default: DEMO): ").strip().upper() or "DEMO"
        run_sample_data_demo(symbol_name)
        
    elif choice == "6":
        # Connection diagnostics
        run_connection_diagnostics()
        
    elif choice == "7":
        # System information
        show_system_information()
        
    else:
        print("❌ Invalid choice. Please select 1-7.")

def run_enhanced_strategy(host, port, symbol):
    """Run enhanced strategy with comprehensive error handling and monitoring"""
    
    print(f"\n🚀 Running Enhanced Triple SMA Strategy")
    print(f"   📡 Connection: {host}:{port}")
    print(f"   📈 Symbol: {symbol}")
    print(f"   🎯 Strategy: Triple SMA (20/50/200)")
    
    # Pre-flight connection check
    print(f"\n🔍 Pre-flight connection check...")
    net_ok, net_msg = conn_mgr.test_network_connection(host, port, timeout=5)
    
    if not net_ok:
        print(f"❌ Pre-flight check failed: {net_msg}")
        retry = input("🔄 Retry anyway? (y/n): ").lower().strip()
        if retry != 'y':
            return
    else:
        print(f"✅ Pre-flight check passed")
    
    # Enhanced IBKR connection with retry logic
    app = EnhancedIBapi()
    
    for attempt in range(3):
        try:
            print(f"\n📡 Connection attempt {attempt + 1}/3...")
            
            app.connect(host, port, clientId=1)
            api_thread = threading.Thread(target=app.run, daemon=True)
            api_thread.start()
            
            # Wait for connection with progress indicator
            timeout = 20
            start_time = time.time()
            
            while app.connection_status not in ["connected", "error"] and time.time() - start_time < timeout:
                elapsed = time.time() - start_time
                if int(elapsed) % 5 == 0 and elapsed > 0:
                    print(f"   ⏳ Connecting... {int(elapsed)}s")
                time.sleep(1)
            
            if app.connection_status == "connected":
                print(f"✅ Connected successfully!")
                break
            else:
                print(f"❌ Attempt {attempt + 1} failed: {app.connection_status}")
                if app.last_error:
                    print(f"   Error: {app.last_error[1]}")
                app.disconnect()
                
                if attempt < 2:
                    print(f"🔄 Retrying in 3 seconds...")
                    time.sleep(3)
                
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} error: {e}")
            if attempt < 2:
                time.sleep(3)
    
    if app.connection_status != "connected":
        print(f"❌ Failed to connect after 3 attempts")
        return
    
    # Request historical data with enhanced error handling
    try:
        contract = create_contract(symbol)
        app.data = []
        app.data_received = False
        app.data_quality_issues = []
        
        print(f"\n📊 Requesting historical data for {symbol}...")
        print(f"   Duration: 2 years")
        print(f"   Bar size: 1 day")
        print(f"   Data type: MIDPOINT")
        
        app.reqHistoricalData(
            reqId=1,
            contract=contract,
            endDateTime='',
            durationStr='2 Y',
            barSizeSetting='1 day',
            whatToShow='MIDPOINT',
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[]
        )
        
        # Wait for data with progress updates
        timeout = 30
        start_time = time.time()
        last_count = 0
        
        while not app.data_received and time.time() - start_time < timeout:
            current_count = len(app.data)
            if current_count != last_count:
                print(f"   📈 Received {current_count} bars...")
                last_count = current_count
            time.sleep(1)
        
        app.disconnect()
        
        if not app.data_received:
            print(f"❌ Data request timeout after {timeout}s")
            return
            
        if len(app.data) < 200:
            print(f"⚠️ Warning: Only {len(app.data)} bars received (need 200+ for SMA200)")
            proceed = input("Continue anyway? (y/n): ").lower().strip()
            if proceed != 'y':
                return
        
        # Process data with enhanced validation
        print(f"\n🧮 Processing {len(app.data)} bars of data...")
        
        # Convert to tuple for caching
        data_tuple = tuple(map(tuple, app.data))
        
        # Calculate strategy with timing
        calc_start = time.time()
        df = calculate_triple_sma_enhanced(data_tuple)
        calc_time = time.time() - calc_start
        
        print(f"⚡ Strategy calculation completed in {calc_time:.3f}s")
        
        # Generate enhanced visualization
        print(f"\n📊 Creating enhanced visualization...")
        create_enhanced_visualization(df, symbol)
        
        # Generate comprehensive analytics
        print(f"\n📈 Generating comprehensive analytics...")
        generate_enhanced_analytics(df, symbol)
        
        # Current signal analysis
        analyze_current_signal(df, symbol)
        
        print(f"\n✅ Enhanced analysis complete for {symbol}!")
        
    except Exception as e:
        print(f"❌ Strategy execution error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            app.disconnect()
        except:
            pass

def generate_enhanced_analytics(df, symbol):
    """Generate enhanced analytics with QuantStats and custom metrics"""
    
    print(f"\n📊 ENHANCED ANALYTICS FOR {symbol}")
    print("=" * 50)
    
    # Extract strategy returns
    strategy_returns = df['strategy_returns'].dropna()
    
    if strategy_returns.empty or strategy_returns.sum() == 0:
        print("⚠️ No strategy returns to analyze")
        return
    
    try:
        # Enhanced performance metrics
        total_return = (1 + strategy_returns).prod() - 1
        annualized_return = qs.stats.cagr(strategy_returns)
        volatility = qs.stats.volatility(strategy_returns, annualize=True)
        sharpe = qs.stats.sharpe(strategy_returns)
        max_dd = qs.stats.max_drawdown(strategy_returns)
        win_rate = qs.stats.win_rate(strategy_returns)
        
        # Custom metrics
        positive_returns = strategy_returns[strategy_returns > 0]
        negative_returns = strategy_returns[strategy_returns < 0]
        avg_win = positive_returns.mean() if len(positive_returns) > 0 else 0
        avg_loss = negative_returns.mean() if len(negative_returns) > 0 else 0
        profit_factor = abs(positive_returns.sum() / negative_returns.sum()) if negative_returns.sum() != 0 else float('inf')
        
        # Trading statistics
        signals = df[df['position'] != 0]
        total_trades = len(signals)
        buy_signals = len(df[df['position'] > 0])
        sell_signals = len(df[df['position'] < 0])
        
        # Display metrics in formatted table
        metrics_data = [
            ["📈 Total Return", f"{total_return:.2%}"],
            ["📊 Annualized Return (CAGR)", f"{annualized_return:.2%}"],
            ["⚡ Sharpe Ratio", f"{sharpe:.2f}"],
            ["📉 Max Drawdown", f"{max_dd:.2%}"],
            ["🎯 Win Rate", f"{win_rate:.2%}"],
            ["📊 Volatility (Ann.)", f"{volatility:.2%}"],
            ["💰 Avg Win", f"{avg_win:.4%}"],
            ["💸 Avg Loss", f"{avg_loss:.4%}"],
            ["🔢 Profit Factor", f"{profit_factor:.2f}"],
            ["🔄 Total Trades", f"{total_trades}"],
            ["🟢 Buy Signals", f"{buy_signals}"],
            ["🔴 Sell Signals", f"{sell_signals}"]
        ]
        
        print(tabulate(metrics_data, headers=["Metric", "Value"], tablefmt="grid"))
        
        # QuantStats visualizations
        print(f"\n📊 Generating QuantStats visualizations...")
        
        # Returns plot
        try:
            qs.plots.returns(strategy_returns, figsize=(12, 6))
            plt.title(f'Cumulative Returns - {symbol}')
            plt.show()
        except Exception as e:
            print(f"⚠️ Could not generate returns plot: {e}")
        
        # Monthly heatmap
        try:
            qs.plots.monthly_heatmap(strategy_returns, figsize=(10, 6))
            plt.title(f'Monthly Returns Heatmap - {symbol}')
            plt.show()
        except Exception as e:
            print(f"⚠️ Could not generate monthly heatmap: {e}")
        
        # Drawdown plot
        try:
            qs.plots.drawdown(strategy_returns, figsize=(12, 4))
            plt.title(f'Strategy Drawdowns - {symbol}')
            plt.show()
        except Exception as e:
            print(f"⚠️ Could not generate drawdown plot: {e}")
        
    except Exception as e:
        print(f"❌ Error generating analytics: {e}")

def analyze_current_signal(df, symbol):
    """Analyze current market signal and conditions"""
    
    print(f"\n🎯 CURRENT SIGNAL ANALYSIS FOR {symbol}")
    print("=" * 50)
    
    # Get latest data
    latest = df.iloc[-1]
    current_price = latest['close']
    current_signal = latest['signal']
    sma20 = latest['sma20']
    sma50 = latest['sma50']
    sma200 = latest['sma200']
    
    # Signal interpretation
    if current_signal == 1:
        signal_text = "🚀 STRONG BUY (Bullish Trend)"
        signal_color = "🟢"
    elif current_signal == -1:
        signal_text = "🔻 STRONG SELL (Bearish Trend)"
        signal_color = "🔴"
    else:
        signal_text = "➡️ NEUTRAL (Mixed Conditions)"
        signal_color = "🟡"
    
    print(f"{signal_color} Current Signal: {signal_text}")
    
    # Price and SMA analysis
    price_data = [
        ["💲 Current Price", f"${current_price:.2f}"],
        ["📈 SMA 20", f"${sma20:.2f}", f"({((current_price/sma20-1)*100):+.1f}%)"],
        ["📊 SMA 50", f"${sma50:.2f}", f"({((current_price/sma50-1)*100):+.1f}%)"],
        ["📉 SMA 200", f"${sma200:.2f}", f"({((current_price/sma200-1)*100):+.1f}%)"]
    ]
    
    print(f"\n📊 Price Analysis:")
    for row in price_data:
        if len(row) == 3:
            print(f"   {row[0]}: {row[1]} {row[2]}")
        else:
            print(f"   {row[0]}: {row[1]}")
    
    # Trend strength analysis
    sma_alignment = "Aligned" if sma20 > sma50 > sma200 or sma20 < sma50 < sma200 else "Mixed"
    trend_strength = "Strong" if sma_alignment == "Aligned" else "Weak"
    
    print(f"\n🎯 Trend Analysis:")
    print(f"   📊 SMA Alignment: {sma_alignment}")
    print(f"   💪 Trend Strength: {trend_strength}")
    
    # Recent performance
    recent_returns = df['strategy_returns'].tail(20)
    recent_performance = recent_returns.mean() * 252  # Annualized
    
    print(f"   📈 Recent Performance (20d): {recent_performance:.2%} annualized")
    
    # Recommendations
    print(f"\n💡 Trading Recommendations:")
    if current_signal == 1:
        print(f"   • Consider LONG position or HOLD existing long")
        print(f"   • Stop loss below SMA 20: ${sma20:.2f}")
        print(f"   • Target: Previous resistance levels")
    elif current_signal == -1:
        print(f"   • Consider SHORT position or CLOSE long")
        print(f"   • Stop loss above SMA 20: ${sma20:.2f}")
        print(f"   • Target: Previous support levels")
    else:
        print(f"   • WAIT for clearer signal")
        print(f"   • Monitor for SMA alignment")
        print(f"   • Avoid new positions in choppy conditions")

def run_sample_data_demo(symbol_name):
    """Run enhanced demo with sample data"""
    
    print(f"\n🎲 ENHANCED SAMPLE DATA DEMO: {symbol_name}")
    print("=" * 50)
    
    # Generate enhanced sample data
    np.random.seed(42)
    
    # Create more realistic sample data with trends and volatility clusters
    start_date = pd.Timestamp('2022-01-01')
    dates = [start_date + pd.Timedelta(days=i) for i in range(600)]
    
    # Generate price series with multiple regimes
    price = 100
    prices = [price]
    trend = 0.0005  # Base trend
    volatility = 0.02
    
    for i in range(1, 600):
        # Add regime changes
        if i == 150:  # Bear market
            trend = -0.001
            volatility = 0.03
        elif i == 300:  # Recovery
            trend = 0.002
            volatility = 0.025
        elif i == 450:  # Consolidation
            trend = 0.0002
            volatility = 0.015
        
        # Generate return with trend and volatility clustering
        daily_return = np.random.normal(trend, volatility)
        
        # Add some mean reversion
        if abs(daily_return) > 0.05:
            daily_return *= 0.5
        
        price = price * (1 + daily_return)
        prices.append(max(price, 10))
    
    # Create OHLCV data
    sample_data = []
    for i, date in enumerate(dates):
        close_price = prices[i]
        high = close_price * np.random.uniform(1.0, 1.03)
        low = close_price * np.random.uniform(0.97, 1.0)
        open_price = prices[i-1] * np.random.uniform(0.98, 1.02) if i > 0 else close_price
        volume = int(np.random.normal(1200000, 400000))
        
        sample_data.append([
            date.strftime('%Y%m%d %H:%M:%S'),
            open_price, high, low, close_price, volume
        ])
    
    # Run strategy
    print(f"📊 Processing {len(sample_data)} bars of sample data...")
    
    data_tuple = tuple(map(tuple, sample_data))
    df = calculate_triple_sma_enhanced(data_tuple)
    
    # Generate visualizations and analytics
    create_enhanced_visualization(df, symbol_name)
    generate_enhanced_analytics(df, symbol_name)
    analyze_current_signal(df, symbol_name)
    
    print(f"\n✅ Enhanced demo complete for {symbol_name}!")

def run_connection_diagnostics():
    """Run comprehensive connection diagnostics"""
    
    print(f"\n🔍 CONNECTION DIAGNOSTICS")
    print("=" * 40)
    
    # Check ngrok status
    print(f"\n1️⃣ ngrok Status Check...")
    ngrok_ok, ngrok_info = conn_mgr.check_ngrok_status()
    
    if ngrok_ok:
        print(f"✅ ngrok is running with active tunnels:")
        for tunnel in ngrok_info:
            print(f"   📡 {tunnel['public_url']} → {tunnel['local_addr']}")
    else:
        print(f"❌ ngrok issue: {ngrok_info}")
    
    # Connection statistics
    print(f"\n2️⃣ Connection Statistics...")
    stats = conn_mgr.get_connection_stats()
    print(f"   {stats}")
    
    # Recent connection history
    if conn_mgr.connection_history:
        print(f"\n3️⃣ Recent Connection Attempts:")
        recent = conn_mgr.connection_history[-5:]  # Last 5 attempts
        for i, conn in enumerate(recent, 1):
            status_icon = "✅" if conn['status'] == 'success' else "❌"
            timestamp = conn['timestamp'].strftime('%H:%M:%S')
            print(f"   {status_icon} {timestamp} - {conn['host']}:{conn['port']} - {conn['status']}")
    
    # System information
    print(f"\n4️⃣ System Information:")
    print(f"   🐍 Python version: {pd.__version__}")
    print(f"   📊 pandas version: {pd.__version__}")
    print(f"   📈 matplotlib version: {plt.matplotlib.__version__}")
    print(f"   📊 quantstats version: {qs.__version__}")

def show_system_information():
    """Show comprehensive system information"""
    
    print(f"\n📋 ENHANCED SYSTEM INFORMATION")
    print("=" * 50)
    
    info_data = [
        ["🎯 Strategy", "Triple SMA (20/50/200)"],
        ["📊 Analytics", "QuantStats + Custom Metrics"],
        ["🔗 API", "Interactive Brokers TWS/Gateway"],
        ["🌐 Tunnel", "ngrok TCP tunnel"],
        ["🐍 Platform", "Google Colab"],
        ["💾 Caching", "functools.lru_cache"],
        ["📈 Visualization", "Enhanced multi-subplot charts"],
        ["🔍 Validation", "Comprehensive data quality checks"],
        ["🔄 Retry Logic", "3-attempt connection retry"],
        ["📊 Progress", "Real-time status updates"]
    ]
    
    print(tabulate(info_data, headers=["Feature", "Description"], tablefmt="grid"))
    
    print(f"\n📋 Strategy Rules:")
    rules_data = [
        ["🟢 BUY Signal", "Price > SMA20 > SMA50 > SMA200"],
        ["🔴 SELL Signal", "Price < SMA20 < SMA50 < SMA200"],
        ["➡️ NEUTRAL", "Mixed or transitional conditions"]
    ]
    
    print(tabulate(rules_data, headers=["Signal", "Condition"], tablefmt="grid"))
    
    print(f"\n💡 Usage Tips:")
    tips = [
        "• Start with guided setup for first-time users",
        "• Use paper trading account for testing",
        "• Ensure stable ngrok tunnel before trading",
        "• Monitor connection statistics regularly",
        "• Check data quality metrics before trading",
        "• Use sample data demo to understand features"
    ]
    
    for tip in tips:
        print(f"   {tip}")

print("🎮 Enhanced main execution system ready!")
print("\n" + "="*60)
print("✅ ALL ENHANCED COMPONENTS LOADED SUCCESSFULLY!")
print("="*60)
print("🚀 Ready to run enhanced system! Execute the next cell to start.")

# ============================================================================
# CELL 11: Execute Enhanced Trading System
# ============================================================================

# Run the enhanced system
enhanced_triple_sma_system()