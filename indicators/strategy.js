// =============================================
// Capitalize.ai Integration Implementation
// =============================================

// Strategy Configuration
const config = {
    initialCapital: 6000,
    stopTradingBalance: 5400,  // Stop trading if balance falls below this
    maxRiskPerTrade: 0.02,     // 2% risk per trade
};

// Main webhook handler for incoming signals
exports.onWebhook = async (data) => {
    // Extract current balance from signal
    const currentBalance = parseFloat(data.signal.split('balance=')[1]);
    
    // Check if balance is below threshold
    if (currentBalance <= config.stopTradingBalance) {
        // Close all positions and stop trading
        await closeAllPositions({
            reason: "EMERGENCY_STOP_LOW_BALANCE"
        });
        
        // Send notification about emergency stop
        await sendNotification({
            title: "Emergency Stop",
            message: `Trading stopped - Balance (${currentBalance}) below threshold (${config.stopTradingBalance})`
        });
        
        return;
    }

    // Calculate position size based on risk management
    const riskAmount = currentBalance * config.maxRiskPerTrade;
    const positionSize = calculatePositionSize(riskAmount, data.price);

    // Handle trading signals
    switch(data.signal.split(',')[0]) {
        case "TRIPLE_SMA_BUY":
            if (currentBalance > config.stopTradingBalance) {
                await openLongPosition({
                    symbol: data.symbol,
                    price: data.price,
                    size: positionSize,
                    stopLoss: data.price * 0.98  // 2% stop loss
                });
            }
            break;
            
        case "TRIPLE_SMA_SELL":
        case "EMERGENCY_EXIT":
            await closePosition({
                symbol: data.symbol,
                reason: data.signal
            });
            break;
    }
}

// Helper function for position size calculation
function calculatePositionSize(riskAmount, currentPrice) {
    const stopLossPercent = 0.02; // 2% stop loss
    const riskPerUnit = currentPrice * stopLossPercent;
    return Math.floor(riskAmount / riskPerUnit);
}
