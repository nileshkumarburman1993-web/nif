"""
Angel One API Integration
Handles authentication, order placement, and position management
"""

from SmartApi import SmartConnect
import pyotp
from config import Config

class AngelAPI:
    """Wrapper class for Angel One SmartAPI"""
    
    def __init__(self):
        """Initialize Angel One API client with config credentials"""
        self.api = SmartConnect(api_key=Config.ANGEL_API_KEY)
        self.session = None
        self.logged_in = False
        
    def login(self):
        """Angel One login with TOTP"""
        try:
            totp = pyotp.TOTP(Config.ANGEL_TOTP_SECRET).now()
            data = self.api.generateSession(Config.ANGEL_CLIENT_ID, Config.ANGEL_PASSWORD, totp)
            self.session = data['data']['jwtToken']
            self.logged_in = True
            print("✅ Angel One Login Success")
            return True
        except Exception as e:
            print(f"❌ Login Failed: {e}")
            self.logged_in = False
            return False
    
    def is_logged_in(self):
        """Check if logged in"""
        return self.logged_in
    
    def get_ltp(self, symbol="NIFTY BANK"):
        """Get Last Traded Price"""
        try:
            response = self.api.ltpData("NSE", symbol, "")
            return response['data']['ltp']
        except Exception as e:
            print(f"Error getting LTP: {e}")
            return None
    
    def get_profile(self):
        """Get user profile"""
        try:
            if not self.logged_in:
                return None
            profile = self.api.getProfile(self.session)
            return profile['data'] if profile.get('status') else None
        except Exception as e:
            print(f"Error fetching profile: {e}")
            return None
    
    def place_order(self, symbol, qty, order_type="BUY"):
        """Place Market Order"""
        try:
            if not self.logged_in:
                print("❌ Not logged in")
                return None
                
            params = {
                "variety": "NORMAL",
                "tradingsymbol": symbol,
                "symboltoken": self.get_token(symbol),
                "transactiontype": order_type,
                "exchange": "NFO",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": qty
            }
            order = self.api.placeOrder(params)
            print(f"✅ Order Placed: {order}")
            return order
        except Exception as e:
            print(f"❌ Order Failed: {e}")
            return None
    
    def get_token(self, symbol):
        """Get instrument token from symbol"""
        # Simplified - you need to download Angel's instrument list
        # https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json
        return "99926000"  # Example token for BANKNIFTY
    
    def get_positions(self):
        """Get current positions"""
        try:
            if not self.logged_in:
                return []
            response = self.api.position()
            if response.get('status'):
                return response['data']
            else:
                print(f"Failed to fetch positions: {response.get('message')}")
                return []
        except Exception as e:
            print(f"Error fetching positions: {e}")
            return []
    
    def cancel_order(self, order_id, variety='NORMAL'):
        """Cancel an order"""
        try:
            if not self.logged_in:
                print("❌ Not logged in")
                return None
            response = self.api.cancelOrder(order_id, variety)
            if response.get('status'):
                print(f"✅ Order cancelled: {order_id}")
                return response
            else:
                print(f"❌ Cancellation failed: {response.get('message')}")
                return None
        except Exception as e:
            print(f"Error cancelling order: {e}")
            return None
    
    def get_order_book(self):
        """Get order book"""
        try:
            if not self.logged_in:
                return []
            response = self.api.orderBook()
            if response.get('status'):
                return response['data']
            else:
                print(f"Failed to fetch order book: {response.get('message')}")
                return []
        except Exception as e:
            print(f"Error fetching order book: {e}")
            return []
    
    def logout(self):
        """Logout from Angel One API"""
        try:
            if self.api and self.logged_in:
                self.api.terminateSession(Config.ANGEL_CLIENT_ID)
                self.logged_in = False
                print("✅ Logged out successfully")
                return True
        except Exception as e:
            print(f"Logout error: {e}")
            return False
