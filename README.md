# Triple SMA Trading Strategy with Capital Management

## Overview
This repository contains a complete trading strategy implementation using Triple Simple Moving Average (SMA) crossover with advanced capital management features. The strategy is implemented in Pine Script for TradingView and includes integration with Capitalize.ai for automated trading execution.

## Features
- Triple SMA crossover strategy (20, 50, 200 periods)
- Robust capital management system
- Risk management per trade
- Emergency stop-loss mechanisms
- Real-time balance monitoring
- Automated position sizing
- Integration with Capitalize.ai for execution

## Components

### 1. TradingView Strategy (Pine Script)
The strategy uses three Simple Moving Averages:
- 20-period SMA (short-term trend)
- 50-period SMA (intermediate trend)
- 200-period SMA (long-term trend)

#### Risk Management Parameters
- Initial Capital: $6,000
- Maximum Loss: 30%
- Stop Trading Balance: $4,200
- Risk Per Trade: 2%

#### Entry Conditions
- Bullish Alignment: SMA20 > SMA50 > SMA200
- Account balance must be above minimum threshold
- No existing position

#### Exit Conditions
- Bearish Alignment: SMA20 < SMA50 < SMA200
- Emergency exit if balance falls below threshold

### 2. Capitalize.ai Integration
The integration script handles:
- Webhook signal processing
- Position size calculation
- Trade execution
- Emergency stop mechanisms
- Real-time balance monitoring

## Setup Instructions

### TradingView Setup
1. Open TradingView Pine Script Editor
2. Copy and paste the Pine Script code
3. Configure initial parameters:
   - Initial capital
   - Maximum loss percentage
   - Stop trading balance
   - Risk per trade percentage
4. Add strategy to chart and enable alerts

### Capitalize.ai Setup
1. Create a new strategy in Capitalize.ai
2. Copy the integration code
3. Configure webhook settings:
   ```json
   {
     "initialCapital": 6000,
     "stopTradingBalance": 4200,
     "maxRiskPerTrade": 0.02
   }
   ```
4. Set up alert routing from TradingView to Capitalize.ai

## Alert Messages Format
The strategy generates the following alert messages:
- Buy Signal: `TRIPLE_SMA_BUY,balance=<current_balance>`
- Sell Signal: `TRIPLE_SMA_SELL,balance=<current_balance>`
- Emergency Exit: `EMERGENCY_EXIT,balance=<current_balance>`

## Risk Warning
Trading involves substantial risk of loss:
- Always start with a small position size
- Thoroughly backtest the strategy before live trading
- Monitor the strategy performance regularly
- Ensure your broker supports the required order types
- Never risk more than you can afford to lose

## Maintenance
- Regularly check and adjust risk parameters
- Monitor strategy performance metrics
- Update stop-loss levels based on market volatility
- Verify webhook connectivity
- Test emergency stop mechanisms periodically

## Troubleshooting
Common issues and solutions:
1. Webhook Connection Issues
   - Verify API keys
   - Check network connectivity
   - Confirm alert message format

2. Position Sizing Errors
   - Verify account balance
   - Check risk calculation parameters
   - Ensure sufficient margin available

3. Emergency Stop Not Triggering
   - Verify balance threshold settings
   - Check alert routing
   - Test emergency stop functionality

## Support
For technical issues:
- Review TradingView Pine Script documentation
- Check Capitalize.ai API documentation
- Test strategy in paper trading mode first

## Version History
- v1.0.0: Initial release
  - Triple SMA strategy implementation
  - Capital management integration
  - Capitalize.ai webhook setup

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.