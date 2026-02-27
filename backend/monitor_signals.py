"""
Real-time Signal Monitor
Continuously monitors market and displays trading signals
"""

import time
from datetime import datetime
from strategy import TradingStrategy
from config import *

def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def display_analysis(analysis, symbol):
    """Display formatted analysis"""
    clear_screen()
    
    print("=" * 70)
    print(f"📊 LIVE TRADING SIGNALS - {symbol}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    if not analysis:
        print("❌ Failed to fetch market data")
        return
    
    # Market Overview
    print("📈 MARKET OVERVIEW")
    print("-" * 70)
    print(f"   Current Price:     ₹{analysis['current_price']}")
    print(f"   PCR:              {analysis['pcr']}")
    print(f"   Max Pain:         {analysis['max_pain']}")
    print(f"   Heavy Call:       {analysis['heavy_call']}")
    print(f"   Heavy Put:        {analysis['heavy_put']}")
    print()
    
    # Market Sentiment
    pcr = analysis['pcr']
    if pcr < PCR_BULLISH:
        sentiment = "🟢 SUPER BULLISH"
        sentiment_desc = f"PCR {pcr} < {PCR_BULLISH}"
    elif pcr > PCR_BEARISH:
        sentiment = "🔴 SUPER BEARISH"
        sentiment_desc = f"PCR {pcr} > {PCR_BEARISH}"
    else:
        sentiment = "🟡 NEUTRAL"
        sentiment_desc = f"{PCR_BULLISH} < PCR {pcr} < {PCR_BEARISH}"
    
    print("💭 SENTIMENT ANALYSIS")
    print("-" * 70)
    print(f"   {sentiment}")
    print(f"   {sentiment_desc}")
    print()
    
    # Trading Signal
    signal = analysis['signal']
    print("⚡ TRADING SIGNAL")
    print("-" * 70)
    
    if signal['action'] == 'WAIT':
        print("   ⏸️  NO SIGNAL - Wait for better setup")
    else:
        print(f"   Action:       {signal['action']} {signal['type']}")
        print(f"   Entry:        ₹{signal['entry']}")
        print(f"   Target:       ₹{signal['target']} ({signal['target'] - signal['entry']} points)")
        print(f"   Stop Loss:    ₹{signal['sl']} ({abs(signal['entry'] - signal['sl'])} points)")
        print(f"   Confidence:   {signal['confidence']}% 📊")
        
        # Position sizing
        risk_amount = CAPITAL_PER_TRADE * (RISK_PERCENT / 100)
        sl_points = abs(signal['entry'] - signal['sl'])
        qty = int(risk_amount / sl_points) if sl_points > 0 else DEFAULT_QUANTITY
        
        print()
        print("💼 POSITION SIZE")
        print(f"   Capital:      ₹{CAPITAL_PER_TRADE}")
        print(f"   Risk:         ₹{risk_amount} ({RISK_PERCENT}%)")
        print(f"   Quantity:     {qty} lots")
    
    print()
    print("=" * 70)
    print("Press Ctrl+C to stop monitoring")
    print("=" * 70)

def main():
    """Main monitoring loop"""
    print("🚀 Starting Signal Monitor...")
    print("⏳ Initializing strategy...")
    
    strategy = TradingStrategy()
    
    symbol = "BANKNIFTY"  # Change to NIFTY or FINNIFTY if needed
    refresh_interval = 30  # seconds
    
    print(f"✅ Monitoring {symbol} (refresh every {refresh_interval}s)")
    print("Press Ctrl+C to stop")
    time.sleep(2)
    
    try:
        while True:
            # Analyze market
            analysis = strategy.analyze_market(symbol)
            
            # Display results
            display_analysis(analysis, symbol)
            
            # Wait before next refresh
            time.sleep(refresh_interval)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping monitor...")
        strategy.angel.logout()
        print("✅ Logged out. Goodbye!")

if __name__ == "__main__":
    main()
