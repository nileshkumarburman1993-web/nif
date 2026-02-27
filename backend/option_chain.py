"""
NSE Option Chain Scraper - Pandas-Free Version
Fetches real-time option chain data from NSE website
"""

import requests
from bs4 import BeautifulSoup

class OptionChain:
    """Scraper for NSE Option Chain data - No pandas dependency"""
    
    def __init__(self):
        """Initialize the option chain scraper"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
    
    def get_nse_data(self, symbol="NIFTY"):
        """Fetch Option Chain from NSE"""
        try:
            url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
            self.session.get("https://www.nseindia.com", headers=self.headers, timeout=10)
            response = self.session.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            if 'records' in data and 'data' in data['records']:
                return data['records']['data']
            return None
        except Exception as e:
            print(f"NSE Error: {e}")
            return None
    
    def calculate_pcr(self, data):
        """Calculate PCR from option chain"""
        try:
            if not data:
                return 0
            
            total_put_oi = 0
            total_call_oi = 0
            
            for option in data:
                if 'PE' in option:
                    total_put_oi += option['PE'].get('openInterest', 0)
                if 'CE' in option:
                    total_call_oi += option['CE'].get('openInterest', 0)
            
            pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0
            return round(pcr, 2)
        except Exception as e:
            print(f"PCR calculation error: {e}")
            return 0
    
    def get_max_pain(self, data):
        """Calculate Max Pain Strike"""
        try:
            if not data:
                return 0
            
            strikes = list(set([opt.get('strikePrice', 0) for opt in data if 'strikePrice' in opt]))
            strikes.sort()
            
            min_pain = float('inf')
            max_pain_strike = 0
            
            for strike in strikes:
                total_pain = 0
                
                for opt in data:
                    opt_strike = opt.get('strikePrice', 0)
                    
                    if 'CE' in opt and opt_strike > strike:
                        ce_oi = opt['CE'].get('openInterest', 0)
                        total_pain += (opt_strike - strike) * ce_oi
                    
                    if 'PE' in opt and opt_strike < strike:
                        pe_oi = opt['PE'].get('openInterest', 0)
                        total_pain += (strike - opt_strike) * pe_oi
                
                if total_pain < min_pain:
                    min_pain = total_pain
                    max_pain_strike = strike
            
            return int(max_pain_strike) if max_pain_strike else 0
        except Exception as e:
            print(f"Max pain calculation error: {e}")
            return 0
    
    def get_heavy_strikes(self, data):
        """Get highest OI strikes"""
        try:
            if not data:
                return 0, 0
            
            max_call_oi = 0
            max_put_oi = 0
            heavy_call = 0
            heavy_put = 0
            
            for option in data:
                strike = option.get('strikePrice', 0)
                
                if 'CE' in option:
                    ce_oi = option['CE'].get('openInterest', 0)
                    if ce_oi > max_call_oi:
                        max_call_oi = ce_oi
                        heavy_call = strike
                
                if 'PE' in option:
                    pe_oi = option['PE'].get('openInterest', 0)
                    if pe_oi > max_put_oi:
                        max_put_oi = pe_oi
                        heavy_put = strike
            
            return int(heavy_call), int(heavy_put)
        except Exception as e:
            print(f"Heavy strikes calculation error: {e}")
            return 0, 0
    
    # Legacy compatibility methods
    def fetch_option_chain(self, symbol='NIFTY', expiry=None):
        """Legacy method for compatibility"""
        return self.get_nse_data(symbol)
