# Triple SMA Indicator for TradingView

A custom TradingView indicator that displays three Simple Moving Averages (SMA) with different periods to help identify trends and potential support/resistance levels.

## Overview

This indicator plots three SMAs on your chart:
- Short-term SMA (20 periods) - Blue line
- Medium-term SMA (50 periods) - Orange line
- Long-term SMA (200 periods) - Red line

## Features

- Clean, easy-to-read visualization
- Color-coded moving averages for quick trend identification
- Customizable line widths and colors
- Works on all timeframes
- Compatible with all trading instruments (stocks, forex, crypto, etc.)

## Installation

1. Open TradingView's Pine Editor
2. Copy and paste the indicator code
3. Click "Save" and give your indicator a name
4. Click "Add to Chart"

## Pine Script Code

```pinescript
//@version=5
indicator("Triple SMA", overlay=true)

// Calculate SMAs
sma20 = ta.sma(close, 20)
sma50 = ta.sma(close, 50)
sma200 = ta.sma(close, 200)

// Plot SMAs with specified colors
plot(sma20, color=color.new(#3177e0, 0), linewidth=2, title="SMA 20")  // Blue
plot(sma50, color=color.new(#ff9800, 0), linewidth=2, title="SMA 50")  // Orange
plot(sma200, color=color.new(#f44336, 0), linewidth=2, title="SMA 200")  // Red
```

## Usage

The Triple SMA indicator can be used to:
- Identify current market trend
- Spot potential support and resistance levels
- Find potential entry and exit points
- Confirm trend changes

### Common Signals

1. **Trend Direction**
   - Price above all SMAs = Strong uptrend
   - Price below all SMAs = Strong downtrend
   - Price between SMAs = Consolidation or trend transition

2. **Support/Resistance**
   - SMAs often act as dynamic support/resistance levels
   - 200 SMA is particularly important for long-term trend analysis

3. **Golden/Death Cross**
   - Golden Cross: 50 SMA crosses above 200 SMA (bullish)
   - Death Cross: 50 SMA crosses below 200 SMA (bearish)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

ET CHEAH

## Disclaimer

This indicator is for informational purposes only. It should not be considered financial advice. Always do your own research and consider your risk tolerance before trading.