# Enhanced IBKR Trading System v2.0

A comprehensive algorithmic trading system for Interactive Brokers (IBKR) that can be run in Google Colab with advanced technical analysis, risk management, and multi-indicator strategies.

## 🚀 Features

### Enhanced Strategy Components
- **Triple SMA Strategy**: 20, 50, and 200-day Simple Moving Averages with trend confirmation
- **RSI Confirmation**: 14-period Relative Strength Index for momentum filtering
- **Volume Analysis**: Volume spike detection with moving average comparison
- **Signal Strength Calculation**: 0-100% confidence rating for each signal
- **ATR-based Stop Losses**: Automatic stop loss recommendations using Average True Range

### Advanced Risk Management
- **Position Sizing**: Automated calculation based on 2% account risk rule
- **Portfolio Allocation**: Intelligent position sizing recommendations
- **Risk Metrics**: Real-time risk assessment and portfolio exposure analysis
- **Stop Loss Integration**: Dynamic stop loss levels based on market volatility

### Comprehensive Analysis Tools
- **Multi-Symbol Analysis**: Compare signals across multiple stocks simultaneously
- **4-Panel Dashboard**: Price charts, RSI, volume analysis, and signal strength visualization
- **Performance Metrics**: Detailed backtesting results with win/loss ratios
- **Market Hours Detection**: Automatic trading hours validation

### User Experience
- **Interactive Menu System**: Easy-to-use command-line interface
- **Account Summary**: Quick account balance and position overview
- **Real-time Logging**: Detailed operation logs with timestamps
- **Error Recovery**: Robust error handling with automatic retry mechanisms

## 📋 Requirements

### Software Dependencies
```python
# Core packages
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
threading
datetime
logging

# IBKR API
ibapi>=9.81.1
ib_insync>=0.9.86

# Optional (backup data source)
yfinance>=0.1.87
```

### IBKR Setup
1. **TWS or IB Gateway** installed and configured
2. **API connections enabled** in TWS/Gateway settings
3. **Paper trading account** (recommended for testing)
4. **Market data subscriptions** for desired securities

### Network Setup
1. **ngrok** for secure tunneling ([Download here](https://ngrok.com/download))
2. **Stable internet connection**
3. **Port forwarding** capabilities

## 🛠 Installation & Setup

### Step 1: IBKR Configuration
1. Download and install TWS or IB Gateway from IBKR
2. Enable API connections:
   - Go to Global Configuration → API → Settings
   - Enable "ActiveX and Socket Clients"
   - Set Socket port to 7497 (paper trading) or 7496 (live)
   - Enable "Download open orders on connection"

### Step 2: ngrok Setup
```bash
# Download and install ngrok
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip

# Authenticate with your ngrok token
./ngrok authtoken YOUR_AUTH_TOKEN

# Create tunnel to TWS (run this when TWS is active)
./ngrok tcp 7497
```

### Step 3: Google Colab Setup
1. Open [Google Colab](https://colab.research.google.com/)
2. Create a new notebook
3. Copy and paste the provided cells sequentially
4. Run each cell in order

## 🎯 Quick Start Guide

### 1. Start the System
```python
# After running all setup cells
run_enhanced_trading_system()
```

### 2. Enter Connection Details
- **ngrok host**: Copy from ngrok output (e.g., `0.tcp.ngrok.io`)
- **ngrok port**: Copy port number from ngrok output

### 3. Choose Your Operation
```
📋 ENHANCED TRADING SYSTEM MENU
1. 📊 Test Enhanced Strategy (with analysis)
2. 🎯 Execute Trade  
3. 💰 Quick Account Check
4. 📈 Multi-Symbol Analysis
5. ❌ Exit
```

### 4. Strategy Testing Example
```python
# Test Apple stock with full analysis
Symbol: AAPL
Show visualizations: y

# Results will include:
# - 4-panel chart analysis
# - Signal strength ratings
# - Risk management recommendations
# - Current market status
```

## 📊 Strategy Logic

### Signal Generation Rules

#### Buy Signals (Long Entry)
- **Primary**: Price > SMA20 > SMA50 > SMA200
- **RSI Filter**: 35 < RSI < 75 (avoid extreme conditions)
- **Volume Confirmation**: Current volume > 1.2x average volume
- **Proximity Check**: Price within 5% of SMA20

#### Sell Signals (Short Entry/Long Exit)
- **Primary**: Price < SMA20 < SMA50 < SMA200
- **RSI Filter**: 25 < RSI < 65 (avoid extreme conditions)
- **Volume Confirmation**: Current volume > 1.2x average volume
- **Proximity Check**: Price within 5% of SMA20

#### Signal Strength Calculation
```python
signal_strength = (sma_spread * 0.4) + (rsi_strength * 0.3) + (volume_strength * 0.3)
# Strong signals: >60% strength
# Weak signals: ≤60% strength
```

## 💰 Risk Management

### Position Sizing Formula
```python
max_risk_per_trade = account_value * 0.02  # 2% rule
position_size = max_risk_per_trade / stop_loss_distance
max_shares = min(position_size, account_value * 0.10 / stock_price)
```

### Stop Loss Calculation
```python
# For long positions
stop_loss = entry_price - (2 * ATR)

# For short positions  
stop_loss = entry_price + (2 * ATR)
```

## 📈 Visualization Features

### 4-Panel Dashboard
1. **Price Chart**: Candlestick data with SMA overlays and signal markers
2. **RSI Panel**: 14-period RSI with overbought/oversold zones
3. **Volume Analysis**: Volume bars with moving average comparison
4. **Signal Strength**: Time series of signal confidence levels

### Signal Markers
- 🟢 **Strong Buy**: Dark green triangles (>60% strength)
- 🟢 **Weak Buy**: Light green triangles (≤60% strength)
- 🔴 **Strong Sell**: Dark red triangles (>60% strength)  
- 🔴 **Weak Sell**: Light red triangles (≤60% strength)

## 🔧 Advanced Features

### Multi-Symbol Analysis
```python
# Analyze multiple stocks simultaneously
Symbols: AAPL,MSFT,GOOGL,TSLA,AMZN

# Output includes:
# - Comparative signal table
# - Best buy/sell opportunities
# - Risk-adjusted recommendations
```

### Account Management
```python
# Quick account overview
Account Value: $50,000.00
Available Funds: $45,000.00
Buying Power: $90,000.00
Current Positions: AAPL (100 shares @ $150.00)
```

### Export Capabilities
```python
# Save analysis results
save_analysis_results(df, symbol)
# Creates: AAPL_analysis_20250123_143022.csv
```

## ⚠️ Important Disclaimers

1. **Educational Purpose**: This system is for educational and research purposes only
2. **No Financial Advice**: Not intended as investment or financial advice
3. **Paper Trading First**: Always test strategies in paper trading before live trading
4. **Risk Warning**: All trading involves risk of loss
5. **Professional Consultation**: Consider consulting a financial advisor

## 🚨 Security Considerations

### ngrok Security
- Use ngrok's authentication features
- Monitor tunnel access logs
- Consider paid ngrok plans for additional security
- Limit tunnel exposure time

### API Security
- Use paper trading for development
- Implement IP whitelisting when possible
- Monitor API usage and connections
- Keep API credentials secure

## 🔍 Troubleshooting

### Common Issues

#### Connection Problems
```
❌ Failed to connect to TWS
Solutions:
1. Verify TWS/Gateway is running
2. Check API settings are enabled
3. Confirm ngrok tunnel is active
4. Test local connection first
```

#### Data Issues
```
❌ Insufficient historical data
Solutions:
1. Verify market data subscriptions
2. Check symbol spelling
3. Ensure adequate trading history
4. Try different time periods
```

#### Installation Problems
```
❌ Package import errors
Solutions:
1. Re-run installation cells
2. Restart Colab runtime
3. Check Python version compatibility
4. Clear pip cache
```

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Additional Resources

### IBKR Documentation
- [TWS API Documentation](https://interactivebrokers.github.io/tws-api/)
- [IB Gateway Setup Guide](https://www.interactivebrokers.com/en/index.php?f=16457)
- [Paper Trading Account](https://www.interactivebrokers.com/en/index.php?f=1286)

### Technical Analysis
- [Moving Average Strategies](https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp)
- [RSI Indicator Guide](https://www.investopedia.com/terms/r/rsi.asp)
- [Volume Analysis](https://www.investopedia.com/terms/v/volume.asp)

### Risk Management
- [Position Sizing Strategies](https://www.investopedia.com/articles/trading/09/position-size-and-capital-risk.asp)
- [Stop Loss Orders](https://www.investopedia.com/terms/s/stop-lossorder.asp)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Strategy optimizations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or support:
1. Check the troubleshooting section
2. Review IBKR documentation
3. Open an issue on GitHub
4. Consult the community forums

---

**Remember**: Always practice responsible trading and never risk more than you can afford to lose. This system is a tool to assist with analysis and execution, but trading decisions remain your responsibility.