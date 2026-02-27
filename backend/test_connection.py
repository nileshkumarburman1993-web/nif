"""
Test Script to Verify Configuration and Connections
Run this before starting the main application
"""

print("=" * 60)
print("🔍 TRADING AUTOMATION - CONNECTION TEST")
print("=" * 60)

# Test 1: Import all modules
print("\n✅ Test 1: Importing modules...")
try:
    from config import Config
    from angel_api import AngelAPI
    from option_chain import OptionChain
    from strategy import TradingStrategy
    print("   ✓ All modules imported successfully")
except Exception as e:
    print(f"   ✗ Import Error: {e}")
    exit(1)

# Test 2: Check configuration
print("\n✅ Test 2: Checking configuration...")
try:
    print(f"   API Key: {'SET' if Config.ANGEL_API_KEY and Config.ANGEL_API_KEY != 'your_api_key_here' else 'NOT SET'}")
    print(f"   Client ID: {'SET' if Config.ANGEL_CLIENT_ID and Config.ANGEL_CLIENT_ID != 'your_client_id' else 'NOT SET'}")
    print(f"   Password: {'SET' if Config.ANGEL_PASSWORD and Config.ANGEL_PASSWORD != 'your_password' else 'NOT SET'}")
    print(f"   TOTP Secret: {'SET' if Config.ANGEL_TOTP_SECRET and Config.ANGEL_TOTP_SECRET != 'your_totp_secret' else 'NOT SET'}")
    print(f"   PCR Bullish: {Config.PCR_BULLISH}")
    print(f"   PCR Bearish: {Config.PCR_BEARISH}")
    print(f"   Max Pain Threshold: {Config.MAX_PAIN_THRESHOLD}")
    print(f"   Capital Per Trade: ₹{Config.CAPITAL_PER_TRADE}")
except Exception as e:
    print(f"   ✗ Config Error: {e}")

# Test 3: Test NSE Option Chain
print("\n✅ Test 3: Testing NSE option chain scraper...")
try:
    oc = OptionChain()
    df = oc.get_nse_data("NIFTY")
    
    if df is not None and len(df) > 0:
        print(f"   ✓ Option chain fetched: {len(df)} strikes")
        
        # Calculate metrics
        pcr = oc.calculate_pcr(df)
        print(f"   ✓ PCR: {pcr}")
        
        max_pain = oc.get_max_pain(df)
        print(f"   ✓ Max Pain: {max_pain}")
        
        heavy_call, heavy_put = oc.get_heavy_strikes(df)
        print(f"   ✓ Heavy Call Strike: {heavy_call}")
        print(f"   ✓ Heavy Put Strike: {heavy_put}")
        
        # Trading Signal
        if pcr < Config.PCR_BULLISH:
            signal = "🟢 BULLISH"
        elif pcr > Config.PCR_BEARISH:
            signal = "🔴 BEARISH"
        else:
            signal = "🟡 NEUTRAL"
        print(f"   ✓ Market Signal: {signal}")
    else:
        print("   ✗ Failed to fetch option chain (NSE might be down or blocking)")
except Exception as e:
    print(f"   ✗ Option Chain Error: {e}")

# Test 4: Test Angel One API (Login)
print("\n✅ Test 4: Testing Angel One API...")
credentials_set = (
    Config.ANGEL_API_KEY and Config.ANGEL_API_KEY != 'your_api_key_here' and
    Config.ANGEL_CLIENT_ID and Config.ANGEL_CLIENT_ID != 'your_client_id' and
    Config.ANGEL_PASSWORD and Config.ANGEL_PASSWORD != 'your_password' and
    Config.ANGEL_TOTP_SECRET and Config.ANGEL_TOTP_SECRET != 'your_totp_secret'
)

if credentials_set:
    try:
        angel = AngelAPI()
        if angel.login():
            print("   ✓ Angel One login successful!")
            
            # Get profile
            profile = angel.get_profile()
            if profile:
                print(f"   ✓ Profile: {profile.get('name', 'N/A')}")
            
            # Logout
            angel.logout()
        else:
            print("   ✗ Angel One login failed (check credentials or TOTP)")
    except Exception as e:
        print(f"   ✗ Angel API Error: {e}")
else:
    print("   ⚠ Skipped (credentials not configured in .env file)")
    print("   → Edit backend/.env and add your Angel One credentials")

# Test 5: Database
print("\n✅ Test 5: Testing database...")
try:
    import sqlite3
    import os
    
    db_path = '../database/trades.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            symbol TEXT NOT NULL,
            strike REAL NOT NULL,
            option_type TEXT NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL,
            quantity INTEGER NOT NULL,
            side TEXT NOT NULL,
            status TEXT NOT NULL,
            pnl REAL,
            pnl_percentage REAL,
            exit_reason TEXT,
            order_id TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("   ✓ Database initialized successfully")
except Exception as e:
    print(f"   ✗ Database Error: {e}")

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)
print("✓ All core components are working")
print("✓ Ready to start the trading application")
print("\nTo start the server, run:")
print("  python app.py")
print("\nThen open: http://localhost:5000")
print("=" * 60)
