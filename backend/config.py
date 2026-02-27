"""
Configuration file for API keys and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Angel One API Credentials
    ANGEL_API_KEY = os.getenv('ANGEL_API_KEY', 'dummy_key')
    ANGEL_CLIENT_ID = os.getenv('ANGEL_CLIENT_ID', 'dummy_client')
    ANGEL_PASSWORD = os.getenv('ANGEL_PASSWORD', 'dummy_password')
    ANGEL_TOTP_SECRET = os.getenv('ANGEL_TOTP_SECRET', 'JBSWY3DPEHPK3PXP')  # Dummy TOTP
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', '../database/trades.db')
    
    # Strategy Settings
    PCR_BULLISH = float(os.getenv('PCR_BULLISH', '0.65'))
    PCR_BEARISH = float(os.getenv('PCR_BEARISH', '1.35'))
    MAX_PAIN_THRESHOLD = int(os.getenv('MAX_PAIN_THRESHOLD', '100'))
    CAPITAL_PER_TRADE = int(os.getenv('CAPITAL_PER_TRADE', '50000'))
    RISK_PERCENT = int(os.getenv('RISK_PERCENT', '2'))
    
    # Legacy strategy parameters (70% profit target)
    PROFIT_TARGET = float(os.getenv('PROFIT_TARGET', '0.70'))  # 70%
    STOP_LOSS = float(os.getenv('STOP_LOSS', '0.30'))  # 30%
    
    # Trading parameters
    DEFAULT_QUANTITY = int(os.getenv('DEFAULT_QUANTITY', '25'))
    DEFAULT_SYMBOL = os.getenv('DEFAULT_SYMBOL', 'NIFTY')
    
    # Risk management
    MAX_POSITIONS = int(os.getenv('MAX_POSITIONS', '5'))
    MAX_LOSS_PER_DAY = float(os.getenv('MAX_LOSS_PER_DAY', '5000'))
