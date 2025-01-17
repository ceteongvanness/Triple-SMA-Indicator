// =============================================
// Capitalize.ai Integration Implementation
// =============================================

// Strategy Configuration
const config = {
    initialCapital: 6000,
    stopTradingBalance: 5400,  // Stop trading if balance falls below 10% loss
    maxRiskPerTrade: 0.02,     // 2% risk per trade
    stopLossPercent: 0.02      // 2% stop loss per trade
};

// Main webhook handler for incoming signals
exports.onWebhook = async (data) => {
    try {
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
                        stopLoss: calculateStopLoss(data.price),
                        meta: {
                            strategy: "Triple SMA",
                            entryBalance: currentBalance
                        }
                    });
                    
                    // Log entry for monitoring
                    console.log(`Opening long position: ${data.symbol}, Size: ${positionSize}, Entry: ${data.price}`);
                }
                break;
                
            case "TRIPLE_SMA_SELL":
                await closePosition({
                    symbol: data.symbol,
                    reason: "SIGNAL_EXIT",
                    meta: {
                        exitType: "Regular",
                        exitBalance: currentBalance
                    }
                });
                break;
                
            case "EMERGENCY_EXIT":
                await closePosition({
                    symbol: data.symbol,
                    reason: "EMERGENCY_EXIT",
                    meta: {
                        exitType: "Emergency",
                        exitBalance: currentBalance
                    }
                });
                break;
        }
    } catch (error) {
        console.error("Error in webhook handler:", error);
        await sendNotification({
            title: "Strategy Error",
            message: `Error executing strategy: ${error.message}`,
            type: "error"
        });
    }
}

// Helper function for position size calculation
function calculatePositionSize(riskAmount, currentPrice) {
    const riskPerUnit = currentPrice * config.stopLossPercent;
    return Math.floor(riskAmount / riskPerUnit);
}

// Helper function to calculate stop loss price
function calculateStopLoss(entryPrice) {
    return entryPrice * (1 - config.stopLossPercent);
}

// Helper function to validate balance
function isValidBalance(balance) {
    return balance && !isNaN(balance) && balance > 0;
}

// Export configuration and helper functions for testing
module.exports = {
    config,
    calculatePositionSize,
    calculateStopLoss,
    isValidBalance
};
