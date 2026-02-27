"""
Example Usage of Trading Strategy
Demonstrates how to use the PCR-based trading strategy
"""

from strategy import TradingStrategy
from config import *

print("=" * 60)
print("📊 PCR-BASED TRADING STRATEGY - EXAMPLE")
print("=" * 60)

# Initialize strategy
print("\n🔧 Initializing strategy...")
strategy = TradingStrategy()

# Analyze market for BANKNIFTY
print("\n📈 Analyzing BANKNIFTY market...")
analysis = strategy.analyze_market("BANKNIFTY")

if analysis:
    print("\n" + "=" * 60)
    print("📊 MARKET ANALYSIS RESULTS")
    print("=" * 60)
    print(f"📍 Current Price: {analysis['current_price']}")
    print(f"📊 PCR (Put-Call Ratio): {analysis['pcr']}")
    print(f"🎯 Max Pain: {analysis['max_pain']}")
    print(f"📞 Heavy Call Strike: {analysis['heavy_call']}")
    print(f"📉 Heavy Put Strike: {analysis['heavy_put']}")
    print()
    
    # Interpret PCR
    if analysis['pcr'] < PCR_BULLISH:
        sentiment = "🟢 SUPER BULLISH"
    elif analysis['pcr'] > PCR_BEARISH:
        sentiment = "🔴 SUPER BEARISH"
    else:
        sentiment = "🟡 NEUTRAL/RANGE-BOUND"
    
    print(f"Market Sentiment: {sentiment}")
    print()
    
    # Signal
    signal = analysis['signal']
    print("=" * 60)
    print("⚡ TRADING SIGNAL")
    print("=" * 60)
    
    if signal['action'] == 'WAIT':
        print("⏸️  Action: WAIT (No clear setup)")
        print("   No trade signal at this time")
    else:
        print(f"🎯 Action: {signal['action']}")
        print(f"📌 Type: {signal['type']} (Call/Put)")
        print(f"💰 Entry: {signal['entry']}")
        print(f"🎯 Target: {signal['target']}")
        print(f"🛡️  Stop Loss: {signal['sl']}")
        print(f"📊 Confidence: {signal['confidence']}%")
        print()
        
        # Risk calculation
        risk_amount = CAPITAL_PER_TRADE * (RISK_PERCENT / 100)
        sl_points = abs(signal['entry'] - signal['sl'])
        qty = int(risk_amount / sl_points) if sl_points > 0 else DEFAULT_QUANTITY
        
        print("=" * 60)
        print("💼 POSITION SIZING")
        print("=" * 60)
        print(f"Capital Allocated: ₹{CAPITAL_PER_TRADE}")
        print(f"Risk Percentage: {RISK_PERCENT}%")
        print(f"Risk Amount: ₹{risk_amount}")
        print(f"Stop Loss Points: {sl_points}")
        print(f"Recommended Quantity: {qty} lots")
        print()
        
        # Manual execution prompt
        print("=" * 60)
        print("🚀 EXECUTION")
        print("=" * 60)
        print("To execute this trade, uncomment the line in the code:")
        print("# order = strategy.execute_trade(signal)")
        print()
        print("⚠️  WARNING: This will place a REAL order!")
        print("   Make sure to test in paper trading first.")
        print()
        
        # Uncomment below to auto-execute (USE WITH CAUTION!)
        # order = strategy.execute_trade(signal)
        # print(f"Order Result: {order}")

else:
    print("❌ Failed to analyze market")
    print("   Possible reasons:")
    print("   - NSE website is down")
    print("   - Market is closed")
    print("   - Network issues")

print("=" * 60)
print("✅ Analysis Complete")
print("=" * 60)

# Cleanup
strategy.angel.logout()
print("\n🔓 Logged out from Angel One")
