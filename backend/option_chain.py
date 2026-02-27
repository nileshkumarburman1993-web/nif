NSE Option Chain Scraper - Pandas-Free Version
"""

import requests

class OptionChain:
    """Scraper for NSE Option Chain data"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()

    def get_nse_data(self, symbol="NIFTY"):
        """Fetch Option Chain from NSE"""
        try:
            url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
            self.session.get("https://www.nseindia.com", headers=self.headers)
            response = self.session.get(url, headers=self.headers, timeout=10)
            data = response.json()
            return data.get('records', {}).get('data', [])
        except Exception as e:
            print(f"NSE Error: {e}")
            return []

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
