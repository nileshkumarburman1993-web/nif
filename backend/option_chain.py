"""
NSE Option Chain Scraper - Pandas-Free Version
"""

import requests
import os
import time
from datetime import datetime

class OptionChain:
    """Scraper for NSE Option Chain data"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.nseindia.com/option-chain'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_nse_data(self, symbol="NIFTY"):
        """Fetch Option Chain from NSE - Multiple methods"""
        
        # Method 0: Try Selenium if available (most reliable)
        try:
            from nse_selenium import get_nse_data_selenium, is_selenium_available
            
            if is_selenium_available():
                print("🤖 Selenium available - trying browser automation...")
                selenium_data = get_nse_data_selenium(symbol)
                if selenium_data:
                    return selenium_data
        except Exception as e:
            print(f"Selenium attempt failed: {str(e)[:50]}")
        
        # Method 1: Try NSE official API with better headers
        try:
            print(f"🔄 Attempting to fetch LIVE {symbol} data from NSE...")
            
            session = requests.Session()
            
            # Visit homepage first
            base_url = "https://www.nseindia.com"
            session.get(base_url, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            }, timeout=10)
            
            time.sleep(1)  # Wait for cookies
            
            # Now fetch option chain
            api_url = f"{base_url}/api/option-chain-indices?symbol={symbol}"
            response = session.get(api_url, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Accept': 'application/json,text/plain,*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f'{base_url}/option-chain',
                'X-Requested-With': 'XMLHttpRequest'
            }, timeout=10)
            
            if response.status_code == 200:
                json_data = response.json()
                records = json_data.get('records', {})
                option_data = records.get('data', [])
                
                if option_data and len(option_data) > 0:
                    print(f"✅ SUCCESS! Fetched {len(option_data)} LIVE strikes from NSE")
                    underlying = records.get('underlyingValue', 'N/A')
                    print(f"📊 {symbol} Spot Price: {underlying}")
                    return option_data
                    
        except Exception as e:
            print(f"⚠️ NSE Method 1 Failed: {str(e)[:100]}")
        
        # Method 2: Try alternative endpoint
        try:
            print("🔄 Trying alternative NSE endpoint...")
            session = requests.Session()
            session.get("https://www.nseindia.com", timeout=10)
            time.sleep(0.5)
            
            response = session.get(
                f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json().get('records', {}).get('data', [])
                if data:
                    print(f"✅ Alternative endpoint worked! {len(data)} strikes")
                    return data
        except:
            pass
        
        # Fallback: Use mock data
        print("=" * 60)
        print("⚠️  NSE IS BLOCKING - USING SIMULATED DATA")
        print("=" * 60)
        print("Real NSE data requires one of these solutions:")
        print("1. ✅ Use VPN (Recommended for retail traders)")
        print("2. ✅ Deploy on Indian VPS/Cloud")
        print("3. ✅ Use Selenium browser automation")
        print("4. ✅ Subscribe to paid NSE data feed")
        print("=" * 60)
        
        from mock_data import get_mock_option_data
        return get_mock_option_data(symbol)

    def calculate_pcr(self, data):
        """Calculate PCR without pandas"""
        if not data:
            return 0

        total_put_oi = sum(opt.get('PE', {}).get('openInterest', 0) for opt in data if 'PE' in opt)
        total_call_oi = sum(opt.get('CE', {}).get('openInterest', 0) for opt in data if 'CE' in opt)

        pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0
        return round(pcr, 2)

    def get_max_pain(self, data):
        """Calculate Max Pain without pandas"""
        if not data:
            return 0

        strikes = list(set(opt.get('strikePrice', 0) for opt in data))
        min_pain = float('inf')
        max_pain_strike = 0

        for strike in strikes:
            pain = 0
            for opt in data:
                opt_strike = opt.get('strikePrice', 0)
                if 'CE' in opt and opt_strike >= strike:
                    pain += opt['CE'].get('openInterest', 0) * abs(opt_strike - strike)
                if 'PE' in opt and opt_strike <= strike:
                    pain += opt['PE'].get('openInterest', 0) * abs(strike - opt_strike)

            if pain < min_pain:
                min_pain = pain
                max_pain_strike = strike

        return int(max_pain_strike) if max_pain_strike else 0

    def get_heavy_strikes(self, data):
        """Get highest OI strikes without pandas"""
        if not data:
            return 0, 0

        max_call_oi = 0
        max_put_oi = 0
        heavy_call = 0
        heavy_put = 0

        for opt in data:
            strike = opt.get('strikePrice', 0)

            if 'CE' in opt:
                ce_oi = opt['CE'].get('openInterest', 0)
                if ce_oi > max_call_oi:
                    max_call_oi = ce_oi
                    heavy_call = strike

            if 'PE' in opt:
                pe_oi = opt['PE'].get('openInterest', 0)
                if pe_oi > max_put_oi:
                    max_put_oi = pe_oi
                    heavy_put = strike

        return int(heavy_call), int(heavy_put)

    def fetch_option_chain(self, symbol='NIFTY', expiry=None):
        """Legacy compatibility"""
        return self.get_nse_data(symbol)
