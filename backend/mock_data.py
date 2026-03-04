"""
Mock data provider for testing when NSE API is blocked
"""

def get_mock_option_data(symbol="BANKNIFTY"):
    """Generate mock option chain data"""
    
    # Simulated current price
    if symbol == "BANKNIFTY":
        underlying_value = 48250
        strikes = list(range(47000, 50000, 100))
    elif symbol == "NIFTY":
        underlying_value = 21850
        strikes = list(range(21000, 23000, 50))
    else:
        underlying_value = 20000
        strikes = list(range(19000, 21000, 100))
    
    option_data = []
    
    for strike in strikes:
        # Calculate realistic OI based on distance from ATM
        distance = abs(strike - underlying_value)
        base_oi = max(100000 - (distance * 100), 10000)
        
        # Add some variance
        import random
        ce_oi = int(base_oi * random.uniform(0.8, 1.2))
        pe_oi = int(base_oi * random.uniform(0.8, 1.2))
        
        option_data.append({
            'strikePrice': strike,
            'expiryDate': '06-Mar-2026',
            'underlyingValue': underlying_value,
            'CE': {
                'strikePrice': strike,
                'openInterest': ce_oi,
                'changeinOpenInterest': random.randint(-5000, 5000),
                'pchangeinOpenInterest': round(random.uniform(-10, 10), 2),
                'totalTradedVolume': int(ce_oi * 0.3),
                'impliedVolatility': round(random.uniform(15, 35), 2),
                'lastPrice': max(10, int((underlying_value - strike) + 50) if strike < underlying_value else random.randint(10, 100)),
                'change': round(random.uniform(-50, 50), 2),
                'pChange': round(random.uniform(-20, 20), 2),
                'bidQty': random.randint(25, 150),
                'bidprice': random.uniform(50, 200),
                'askQty': random.randint(25, 150),
                'askPrice': random.uniform(50, 200),
            },
            'PE': {
                'strikePrice': strike,
                'openInterest': pe_oi,
                'changeinOpenInterest': random.randint(-5000, 5000),
                'pchangeinOpenInterest': round(random.uniform(-10, 10), 2),
                'totalTradedVolume': int(pe_oi * 0.3),
                'impliedVolatility': round(random.uniform(15, 35), 2),
                'lastPrice': max(10, int((strike - underlying_value) + 50) if strike > underlying_value else random.randint(10, 100)),
                'change': round(random.uniform(-50, 50), 2),
                'pChange': round(random.uniform(-20, 20), 2),
                'bidQty': random.randint(25, 150),
                'bidprice': random.uniform(50, 200),
                'askQty': random.randint(25, 150),
                'askPrice': random.uniform(50, 200),
            }
        })
    
    return option_data
