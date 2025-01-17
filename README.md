# Triple SMA Trading Strategy with Capital Management

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
- Maximum Loss: 10%
- Stop Trading Balance: $5,400
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

## Files Structure
```
├── README.md
├── triple_sma_strategy.pine    # TradingView Pine Script
├── strategy.js                 # Capitalize.ai integration code
└── LICENSE                     # MIT License file
```

## Setup Instructions

### TradingView Setup
1. Open TradingView Pine Script Editor
2. Copy and paste the Pine Script code
3. Configure initial parameters:
   - Initial capital: $6,000
   - Maximum loss percentage: 10%
   - Stop trading balance: $5,400
   - Risk per trade percentage: 2%
4. Add strategy to chart and enable alerts

### Capitalize.ai Setup
1. Create a new strategy in Capitalize.ai
2. Copy the integration code
3. Configure webhook settings:
   ```json
   {
     "initialCapital": 6000,
     "stopTradingBalance": 5400,
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
- v1.0.1: Updated maximum loss parameters
  - Changed maximum loss from 30% to 10%
  - Adjusted stop trading balance to $5,400
- v1.0.0: Initial release
  - Triple SMA strategy implementation
  - Capital management integration
  - Capitalize.ai webhook setup

## ⚠️ Disclaimer

THIS IS FOR EDUCATIONAL PURPOSES ONLY.

This repository and all its contents are intended solely for educational and research purposes. The code and documentation provided here:

- Is NOT financial advice
- Is NOT a recommendation to buy, sell, or trade any assets
- Should NOT be used for making actual trading decisions
- Does NOT guarantee any returns or performance
- May contain errors or inaccuracies
- Should NOT be used with real money without extensive testing and verification

Trading involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results. Users of this code should:
- Understand the risks involved in trading
- Consult with licensed financial advisors before making any investment decisions
- Never trade with money they cannot afford to lose
- Always conduct their own research and due diligence

The authors and contributors of this repository accept no responsibility for any financial losses or damages incurred from using this code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.