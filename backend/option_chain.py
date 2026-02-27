"""
NSE Option Chain Scraper
Fetches real-time option chain data from NSE website
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

class OptionChain:
    """Scraper for NSE Option Chain data"""
    
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
            self.session.get("https://www.nseindia.com", headers=self.headers)  # Cookie setup
            response = self.session.get(url, headers=self.headers)
            data = response.json()
            
            records = data['records']['data']
            df = pd.DataFrame(records)
            
            return df
        except Exception as e:
            print(f"NSE Error: {e}")
            return None
    
    def calculate_pcr(self, df):
        """Calculate PCR from option chain"""
        total_put_oi = df['PE'].apply(lambda x: x.get('openInterest', 0)).sum()
        total_call_oi = df['CE'].apply(lambda x: x.get('openInterest', 0)).sum()
        pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0
        return round(pcr, 2)
    
    def get_max_pain(self, df):
        """Calculate Max Pain Strike"""
        strikes = df['strikePrice'].unique()
        pain_values = []
        
        for strike in strikes:
            call_pain = df[df['strikePrice'] >= strike]['CE'].apply(
                lambda x: x.get('openInterest', 0) * abs(x.get('strikePrice', 0) - strike)
            ).sum()
            put_pain = df[df['strikePrice'] <= strike]['PE'].apply(
                lambda x: x.get('openInterest', 0) * abs(strike - x.get('strikePrice', 0))
            ).sum()
            pain_values.append(call_pain + put_pain)
        
        max_pain_index = pain_values.index(min(pain_values))
        return int(strikes[max_pain_index])
    
    def get_heavy_strikes(self, df):
        """Get highest OI strikes"""
        call_oi = df['CE'].apply(lambda x: x.get('openInterest', 0))
        put_oi = df['PE'].apply(lambda x: x.get('openInterest', 0))
        
        heavy_call = df.loc[call_oi.idxmax(), 'strikePrice']
        heavy_put = df.loc[put_oi.idxmax(), 'strikePrice']
        
        return int(heavy_call), int(heavy_put)
    
    # Legacy compatibility methods
    def fetch_option_chain(self, symbol='NIFTY', expiry=None):
        """Legacy method for compatibility - returns DataFrame"""
        return self.get_nse_data(symbol)
