# Triple SMA Indicator

## ⚠️ Disclaimer

THIS INDICATOR IS FOR EDUCATIONAL PURPOSES ONLY.

This repository and all its contents are intended solely for educational and research purposes. The code and documentation provided here:

- Is NOT financial advice
- Is NOT a recommendation to buy, sell, or trade any assets
- Should NOT be used for making actual trading decisions
- Does NOT guarantee any returns or performance
- May contain errors or inaccuracies

Trading involves substantial risk of loss. Users should consult with licensed financial advisors before making any investment decisions.

## Overview
The Triple SMA Indicator is a technical analysis tool that plots three Simple Moving Averages (SMAs) with different periods on a price chart. This indicator helps traders identify trend direction and potential reversal points.

## Features
- Plots three Simple Moving Averages:
  - 20-period SMA (short-term trend)
  - 50-period SMA (intermediate trend)
  - 200-period SMA (long-term trend)
- Color-coded for easy visual interpretation
- Compatible with TradingView Pine Script version 6

## Technical Explanation
Simple Moving Averages smooth out price data by calculating the average price over a specified period. The Triple SMA indicator uses three different time periods to help traders:

1. **20-period SMA (Blue)**: Reflects short-term price movements
2. **50-period SMA (Orange)**: Shows intermediate-term trends 
3. **200-period SMA (Red)**: Represents long-term market direction

## Usage Guide

### Installation
1. Open TradingView and navigate to the chart you want to apply this indicator to
2. Click on "Indicators" at the top of the chart
3. Select "Pine Editor" to open the Pine Script editor
4. Copy and paste the provided code
5. Click "Save" and name the indicator
6. Click "Add to Chart" to apply the indicator

### Interpretation
- When the shorter-term SMAs (20, 50) are above the longer-term SMA (200), this generally indicates a bullish trend
- When the shorter-term SMAs cross below the longer-term SMA, this may signal a bearish trend
- The relative positions of these three moving averages can help determine market momentum

## Source Code
```pine
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © cheahengteong

//@version=6
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

## Customization
You can modify this indicator by:
- Changing the SMA periods to match your trading timeframe
- Adjusting colors for better visibility
- Adding alerts for SMA crossovers
- Combining with other indicators for confirmation

## License
This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/