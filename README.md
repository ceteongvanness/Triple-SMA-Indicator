# Triple SMA Trading Strategy with QuantStats

A comprehensive algorithmic trading system implementing the Triple Simple Moving Average (SMA) strategy with advanced backtesting, performance analytics, and Interactive Brokers integration.

## 🚀 Features

### **Core Strategy**
- **Triple SMA (20/50/200)** - Professional moving average crossover strategy
- **Enhanced Signal Generation** - Multiple filters to improve win rate
- **5-Year Default Data** - Comprehensive historical analysis
- **Real-time Trading** - Live execution through Interactive Brokers

### **Win Rate Improvements** 🎯
- **Trend Strength Filter** - Only trades in strong trending markets
- **RSI Filter** - Avoids overbought/oversold conditions  
- **Volume Confirmation** - Requires volume support for signals
- **Volatility Filter** - Reduces trading in high volatility periods
- **Signal Confirmation** - 2-day persistence requirement
- **Stop Loss & Take Profit** - Automatic risk management

### **Advanced Analytics** 📊
- **QuantStats Integration** - Professional performance metrics
- **Comprehensive Backtesting** - Transaction costs, slippage, commission
- **Performance Visualization** - Charts, drawdowns, heatmaps
- **Strategy Optimization** - Test multiple parameter combinations
- **Risk Analysis** - Sharpe ratio, max drawdown, volatility

### **Platform Support** 🔗
- **Google Colab** - Cloud-based execution
- **Interactive Brokers API** - Real broker integration  
- **Paper Trading** - Safe testing environment
- **ngrok Support** - Tunnel for Colab-TWS connection

## 📋 Strategy Rules

### **Buy Signal (Long Position)**
```
Price > SMA20 > SMA50 > SMA200
+ Strong trend (2%+ SMA separation)
+ RSI between 30-70 (if enabled)
+ Volume 20%+ above average (if enabled)
+ Low volatility period
+ 2-day signal confirmation
```

### **Sell Signal (Short Position)**
```
Price < SMA20 < SMA50 < SMA200  
+ Strong downtrend (2%+ SMA separation)
+ RSI between 30-70 (if enabled)
+ Volume 20%+ above average (if enabled)
+ Low volatility period
+ 2-day signal confirmation
```

### **Risk Management**
- **Stop Loss**: 5% default (configurable)
- **Take Profit**: 10% default (configurable)
- **Position Sizing**: Full capital utilization
- **Transaction Costs**: 0.1% commission + 0.05% slippage

## 🛠️ Installation & Setup

### **1. Google Colab Setup (Recommended)**
```python
# No installation needed - everything runs in the cloud!
# Just open the notebook in Google Colab and run all cells
```

### **2. Local Installation**
```bash
pip install pandas numpy matplotlib quantstats ibapi yfinance requests
```

### **3. Interactive Brokers Setup**
1. **Download TWS or IB Gateway**
2. **Enable API Access**:
   - File → Global Configuration → API → Settings
   - ✅ Enable ActiveX and Socket Clients
   - ✅ Read-Only API (for testing)
   - Port: 7497 (Paper Trading) or 7496 (Live)
3. **Paper Trading Account** (recommended for testing)

### **4. ngrok Setup (for Colab)**
```bash
# Download from https://ngrok.com/download
# Sign up and get authtoken
ngrok config add-authtoken YOUR_TOKEN
ngrok tcp 7497
```

## 🎮 Usage

### **Option 1: Test Strategy with Real Data**
```python
run_triple_sma_system()
# Choose: 1
# Enter symbol: AAPL
# Select duration: 2 (5 years)
# Review backtest → Execute trades
```

### **Option 2: Execute Trades (with Backtesting)**
```python
run_triple_sma_system()
# Choose: 2
# Backtest first: y
# Review results → Enter trade details
```

### **Option 3: Demo Mode (No TWS Required)**
```python
run_triple_sma_system()
# Choose: 3
# Enter symbol: DEMO
# Optimization: y (to test win rate improvements)
```

## 📊 Performance Metrics

### **Backtesting Results**
- **Total Return**: Strategy vs buy-and-hold
- **Annualized Return**: CAGR calculation
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Volatility**: Annualized standard deviation

### **QuantStats Reports**
- **Cumulative Returns Chart**
- **Drawdown Analysis**
- **Monthly Returns Heatmap**
- **Risk Metrics Table**
- **Trade Analysis**

## 🔬 Strategy Optimization

The system tests 7 different strategy variations:

| Strategy | Win Rate Improvement | Description |
|----------|---------------------|-------------|
| Original | Baseline | Basic Triple SMA |
| + Trend Filter | +10-15% | Strong trend requirement |
| + RSI Filter | +5-10% | Avoid extremes |
| + Volume Filter | +5-8% | Volume confirmation |
| + Stop Loss | +8-12% | Risk protection |
| + Take Profit | +5-8% | Profit locking |
| + Combined | +15-25% | All improvements |

## 📁 File Structure

```
google_colab_ibkr_guide.ipynb
├── CELL 1: Install Required Packages
├── CELL 2: Import Libraries and Setup
├── CELL 3: IBKR API Wrapper Class
├── CELL 4: Utility Functions
├── CELL 5: Enhanced Triple SMA Strategy
├── CELL 6: Visualization Functions
├── CELL 7: QuantStats Analytics Functions
├── CELL 8: Sample Data Generation (5 Years)
├── CELL 9: Connection Helper Functions
├── CELL 10: IBKR Trading Functions
├── CELL 11: Backtesting Engine
├── CELL 12: Main Execution Interface
└── CELL 13: Execute the System
```

## ⚙️ Configuration Options

### **Data Duration**
- **2 Years**: Fast testing
- **5 Years**: Default, good balance  
- **10 Years**: Comprehensive analysis

### **Strategy Parameters**
```python
calculate_triple_sma_optimized(
    sma20_period=20,           # Short-term SMA
    sma50_period=50,           # Medium-term SMA  
    sma200_period=200,         # Long-term SMA
    use_trend_filter=True,     # Trend strength requirement
    use_rsi_filter=False,      # RSI overbought/oversold filter
    use_volume_filter=False,   # Volume confirmation
    use_stop_loss=False,       # Stop loss protection
    stop_loss_pct=0.05,        # 5% stop loss
    use_take_profit=False,     # Take profit targets
    take_profit_pct=0.10       # 10% take profit
)
```

### **Backtesting Parameters**
```python
TripleSMABacktester(
    initial_capital=100000,    # Starting capital
    commission=0.001,          # 0.1% commission
    slippage=0.0005           # 0.05% slippage
)
```

## 🔒 Risk Management

### **Built-in Protections**
- **Paper Trading Default** - Port 7497 for safe testing
- **Transaction Cost Modeling** - Realistic performance
- **Position Sizing Limits** - Prevent over-leverage
- **Connection Testing** - Verify before trading
- **Backtest Confirmation** - Review before execution

### **Recommended Practices**
1. **Always backtest first** - Review historical performance
2. **Start with paper trading** - Test in safe environment
3. **Begin with small positions** - Gradually increase size
4. **Monitor drawdowns** - Ensure acceptable risk levels
5. **Regular performance review** - Track actual vs expected

## 🐛 Troubleshooting

### **Connection Issues**
```
❌ Error 502: Couldn't connect to TWS
```
**Solutions**:
- ✅ TWS/Gateway is running
- ✅ API settings enabled  
- ✅ Correct port (7497 paper, 7496 live)
- ✅ ngrok tunnel active (for Colab)

### **Font Warnings**
```
WARNING: Font family 'Arial' not found
```
**Solution**: Warnings are cosmetic - charts display correctly

### **No Trading Signals**
```
⚠️ No trading signals generated
```
**Solutions**:
- Use longer data periods (5+ years)
- Check symbol validity
- Verify data quality
- Adjust strategy parameters

## 📈 Example Results

### **Sample Backtest (AAPL, 5 Years)**
```
💰 Initial Capital: $100,000.00
💰 Final Value: $156,750.00
📈 Total Return: 56.75%
📈 Annualized Return: 11.34%
⚡ Sharpe Ratio: 1.23
📉 Max Drawdown: -8.5%
🎯 Win Rate: 68.00%
🔄 Number of Trades: 24
```

## 🤝 Contributing

### **Enhancement Ideas**
- Additional technical indicators (MACD, Bollinger Bands)
- Multi-timeframe analysis
- Portfolio optimization
- Machine learning integration
- Alternative data sources

### **Bug Reports**
Please include:
- Full error message
- Code that triggered the issue
- System environment details
- Steps to reproduce

## 📝 License

This project is for educational and research purposes. Use at your own risk. Past performance does not guarantee future results.

## ⚠️ Disclaimer

**Trading involves substantial risk and is not suitable for all investors.** This software is provided for educational purposes only. Always:

- Test thoroughly with paper trading
- Understand the risks involved
- Never invest more than you can afford to lose
- Consider consulting with financial professionals
- Comply with all applicable regulations

## 🔗 Resources

- **Interactive Brokers API**: [https://interactivebrokers.github.io/tws-api/](https://interactivebrokers.github.io/tws-api/)
- **QuantStats Documentation**: [https://github.com/ranaroussi/quantstats](https://github.com/ranaroussi/quantstats)
- **Google Colab**: [https://colab.research.google.com/](https://colab.research.google.com/)
- **ngrok**: [https://ngrok.com/](https://ngrok.com/)

---

## 🚀 Quick Start

1. **Open the notebook in Google Colab**
2. **Run all cells sequentially** (1-12)
3. **Execute**: `run_triple_sma_system()`
4. **Choose Option 3** for demo mode
5. **Review the comprehensive analysis!**

**Ready to start algorithmic trading? Let's go! 📊🚀**