"""
PCR-based Trading Strategy
Implements PCR, Max Pain, and Heavy Strike analysis for trading signals
"""

import logging
import threading
import time
import sqlite3
from datetime import datetime
from option_chain import OptionChain
from angel_api import AngelAPI
from config import Config

logger = logging.getLogger(__name__)


class TradingStrategy:
    """PCR-based trading strategy implementation"""
    
    def __init__(self, angel_api=None, option_chain_scraper=None):
        """
        Initialize trading strategy
        
        Args:
            angel_api: AngelAPI instance (optional, will create new if not provided)
            option_chain_scraper: OptionChain instance (optional)
        """
        self.oc = option_chain_scraper if option_chain_scraper else OptionChain()
        self.angel = angel_api if angel_api else AngelAPI()
        
        # Login if not already logged in
        if not self.angel.is_logged_in():
            self.angel.login()
        
        self.monitoring = False
        self.monitor_thread = None
        self.db_path = '../database/trades.db'
        self._init_database()
        
        # Strategy parameters from config
        self.profit_target = Config.PROFIT_TARGET  # 70% profit target
        self.stop_loss = Config.STOP_LOSS  # 30% stop loss
        
    def _init_database(self):
        """Initialize SQLite database for trade history"""
        try:
            conn = sqlite3.connect(self.db_path)
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
            logger.info("Database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
    
    def start_monitoring(self, symbol='NIFTY'):
        """
        Start monitoring for trading opportunities
        
        Args:
            symbol: Symbol to monitor
        """
        if self.monitoring:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(symbol,),
            daemon=True
        )
        self.monitor_thread.start()
        logger.info(f"Started monitoring {symbol}")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Stopped monitoring")
    
    def _monitor_loop(self, symbol):
        """
        Main monitoring loop
        
        Args:
            symbol: Symbol to monitor
        """
        while self.monitoring:
            try:
                # Analyze market and generate signals
                analysis = self.analyze_market(symbol)
                
                if not analysis:
                    logger.warning("Failed to analyze market")
                    time.sleep(10)
                    continue
                
                # Log analysis
                logger.info(f"PCR: {analysis['pcr']}, Max Pain: {analysis['max_pain']}, "
                          f"Signal: {analysis['signal']['action']}")
                
                # Execute strategy if signal generated
                if analysis['signal']['action'] != 'WAIT':
                    # Auto-execute can be enabled here
                    # self.execute_trade(analysis['signal'])
                    pass
                
                # Check open positions
                self._monitor_positions()
                
                # Wait before next iteration
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {str(e)}")
                time.sleep(10)
    
    def analyze_market(self, symbol="BANKNIFTY"):
        """Main strategy logic - Now with 15-min candle prediction"""
        try:
            # Try Angel One first for LIVE data
            df = None
            current_price = None
            candles = None
            
            if self.angel.is_logged_in():
                logger.info(f"🔄 Fetching LIVE data from Angel One for {symbol}")
                df = self.angel.get_option_chain(symbol)
                
                if df and len(df) > 0:
                    logger.info(f"✅ Got {len(df)} strikes from Angel One")
                    # Get current price from Angel One data
                    current_price = df[0].get('underlyingValue', 0)
                else:
                    logger.warning("Angel One option chain returned empty, trying NSE...")
                
                # Fetch 15-minute candle data
                candles = self.angel.get_candle_data(symbol, interval="FIFTEEN_MINUTE", count=10)
            
            # Fallback to NSE if Angel One fails
            if not df or len(df) == 0:
                logger.info(f"Trying NSE data for {symbol}...")
                df = self.oc.get_nse_data(symbol)
                
                if not df or len(df) == 0:
                    logger.warning(f"Failed to fetch option chain from both sources")
                    return None
            
            # Calculate metrics
            pcr = self.oc.calculate_pcr(df)
            max_pain = self.oc.get_max_pain(df)
            heavy_call, heavy_put = self.oc.get_heavy_strikes(df)
            
            # Get current price if not already fetched
            if current_price is None or current_price == 0:
                if df and len(df) > 0:
                    current_price = df[0].get('underlyingValue', 0)
                    logger.info(f"Using underlying value from data: {current_price}")
                else:
                    logger.warning("Could not get current price from any source")
                    current_price = 0
            
            # Generate signal with candle prediction
            signal = self.generate_signal_with_candles(pcr, max_pain, current_price, candles)
            
            return {
                'pcr': pcr,
                'max_pain': max_pain,
                'heavy_call': heavy_call,
                'heavy_put': heavy_put,
                'current_price': current_price,
                'signal': signal
            }
        except Exception as e:
            logger.error(f"Error analyzing market: {str(e)}")
            return None
    
    def generate_signal(self, pcr, max_pain, current_price):
        """Generate BUY/SELL/WAIT signal (legacy method)"""
        
        # Validate inputs
        if pcr == 0 or max_pain == 0 or current_price == 0:
            logger.warning(f"Invalid data - PCR: {pcr}, Max Pain: {max_pain}, Price: {current_price}")
            return {'action': 'WAIT', 'confidence': 0, 'reason': 'Insufficient data'}
        
        # Super Bullish
        if pcr <= Config.PCR_BULLISH:
            if current_price < max_pain:
                return {
                    'action': 'BUY',
                    'type': 'CALL',
                    'entry': current_price,
                    'target': max_pain + 100,
                    'sl': current_price - 50,
                    'confidence': 85
                }
        
        # Super Bearish
        elif pcr >= Config.PCR_BEARISH:
            if current_price > max_pain:
                return {
                    'action': 'BUY',
                    'type': 'PUT',
                    'entry': current_price,
                    'target': max_pain - 100,
                    'sl': current_price + 50,
                    'confidence': 80
                }
        
        # Range bound
        else:
            distance = abs(current_price - max_pain)
            if distance > Config.MAX_PAIN_THRESHOLD:
                return {
                    'action': 'BUY',
                    'type': 'CALL' if current_price < max_pain else 'PUT',
                    'entry': current_price,
                    'target': max_pain,
                    'sl': current_price - 50 if current_price < max_pain else current_price + 50,
                    'confidence': 70
                }
        
        return {'action': 'WAIT', 'confidence': 0, 'reason': 'No trading setup'}
    
    def generate_signal_with_candles(self, pcr, max_pain, current_price, candles=None):
        """
        Enhanced signal generation with 15-min candle prediction
        """
        from candle_prediction import predict_next_candle, get_trading_recommendation
        
        # Validate inputs
        if pcr == 0 or max_pain == 0 or current_price == 0:
            logger.warning(f"Invalid data - PCR: {pcr}, Max Pain: {max_pain}, Price: {current_price}")
            return {'action': 'WAIT', 'confidence': 0, 'reason': 'Insufficient data'}
        
        # If candles available, use prediction
        if candles and len(candles) >= 3:
            candle_pred = predict_next_candle(candles, pcr, max_pain, current_price)
            signal = get_trading_recommendation(candle_pred, pcr, max_pain, current_price)
            
            # Add candle prediction info to signal
            signal['candle_prediction'] = {
                'direction': candle_pred['direction'],
                'confidence': candle_pred['confidence'],
                'reason': candle_pred.get('reason', '')
            }
            
            logger.info(f"🕯️ Next candle: {candle_pred['direction']} ({candle_pred['confidence']}%)")
            
            if signal['action'] != 'WAIT':
                return signal
        
        # Fallback to traditional PCR-based signals with relaxed thresholds
        
        # Very Bullish - PCR < 0.8
        if pcr < 0.8:
            return {
                'action': 'BUY',
                'type': 'CALL',
                'entry': current_price,
                'target': current_price + 150,
                'sl': current_price - 75,
                'confidence': 80,
                'reason': f'Very Bullish PCR ({pcr})'
            }
        
        # Very Bearish - PCR > 1.2
        elif pcr > 1.2:
            return {
                'action': 'BUY',
                'type': 'PUT',
                'entry': current_price,
                'target': current_price - 150,
                'sl': current_price + 75,
                'confidence': 75,
                'reason': f'Very Bearish PCR ({pcr})'
            }
        
        # Bullish - PCR < 1.0
        elif pcr < 1.0:
            return {
                'action': 'BUY',
                'type': 'CALL',
                'entry': current_price,
                'target': current_price + 100,
                'sl': current_price - 50,
                'confidence': 65,
                'reason': f'Bullish PCR ({pcr})'
            }
        
        # Bearish - PCR > 1.0
        elif pcr > 1.0:
            return {
                'action': 'BUY',
                'type': 'PUT',
                'entry': current_price,
                'target': current_price - 100,
                'sl': current_price + 50,
                'confidence': 65,
                'reason': f'Bearish PCR ({pcr})'
            }
        
        # Neutral - use Max Pain
        distance = abs(current_price - max_pain)
        if distance > 50:
            if current_price < max_pain:
                return {
                    'action': 'BUY',
                    'type': 'CALL',
                    'entry': current_price,
                    'target': max_pain,
                    'sl': current_price - 50,
                    'confidence': 60,
                    'reason': f'Price below Max Pain by {int(distance)} points'
                }
            else:
                return {
                    'action': 'BUY',
                    'type': 'PUT',
                    'entry': current_price,
                    'target': max_pain,
                    'sl': current_price + 50,
                    'confidence': 60,
                    'reason': f'Price above Max Pain by {int(distance)} points'
                }
        
        return {
            'action': 'WAIT',
            'confidence': 50,
            'reason': 'Market at equilibrium - waiting for better setup'
        }
    
    def execute_trade(self, signal):
        """Auto execute trade"""
        try:
            if signal['action'] == 'WAIT':
                logger.info("No trade setup - waiting for signal")
                return "No trade setup"
            
            # Calculate lot size based on risk
            risk_amount = Config.CAPITAL_PER_TRADE * (Config.RISK_PERCENT / 100)
            sl_points = abs(signal['entry'] - signal['sl'])
            qty = int(risk_amount / sl_points) if sl_points > 0 else Config.DEFAULT_QUANTITY
            
            symbol = f"BANKNIFTY{signal['entry']}{signal['type']}"
            
            order = self.angel.place_order(symbol, qty, "BUY")
            
            # Save trade to database
            if order:
                self._save_trade({
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'strike': signal['entry'],
                    'option_type': signal['type'],
                    'entry_price': signal['entry'],
                    'exit_price': None,
                    'quantity': qty,
                    'side': 'BUY',
                    'status': 'OPEN',
                    'pnl': None,
                    'pnl_percentage': None,
                    'exit_reason': None,
                    'order_id': order.get('data', {}).get('orderid') if isinstance(order, dict) else None
                })
            
            return order
        except Exception as e:
            logger.error(f"Error executing trade: {str(e)}")
            return None
    
    def _analyze_and_trade(self, chain_data):
        """Analyze option chain and execute trades (legacy support)"""
        try:
            symbol = chain_data.get('symbol', 'BANKNIFTY')
            analysis = self.analyze_market(symbol)
            
            if analysis and analysis['signal']['action'] != 'WAIT':
                logger.info(f"Trade signal: {analysis['signal']}")
                # Auto-execute can be enabled here
                # self.execute_trade(analysis['signal'])
                
        except Exception as e:
            logger.error(f"Error in analyze and trade: {str(e)}")
    
    def _monitor_positions(self):
        """Monitor open positions for exit signals"""
        try:
            positions = self.angel.get_positions()
            
            for position in positions:
                # Check profit target and stop loss
                entry_price = float(position.get('averageprice', 0))
                current_price = float(position.get('ltp', 0))
                qty = int(position.get('netqty', 0))
                
                if qty == 0 or entry_price == 0:
                    continue
                
                # Calculate P&L percentage
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
                
                # Check profit target (70%)
                if pnl_pct >= (self.profit_target * 100):
                    logger.info(f"✅ Profit target hit: {position['tradingsymbol']} - {pnl_pct:.2f}%")
                    # Exit position
                    # self._exit_position(position, 'PROFIT_TARGET')
                
                # Check stop loss (30%)
                elif pnl_pct <= -(self.stop_loss * 100):
                    logger.info(f"❌ Stop loss hit: {position['tradingsymbol']} - {pnl_pct:.2f}%")
                    # Exit position
                    # self._exit_position(position, 'STOP_LOSS')
                    
        except Exception as e:
            logger.error(f"Error monitoring positions: {str(e)}")
    
    def _save_trade(self, trade_data):
        """
        Save trade to database
        
        Args:
            trade_data: Dictionary containing trade information
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trades (
                    timestamp, symbol, strike, option_type, entry_price,
                    exit_price, quantity, side, status, pnl, pnl_percentage,
                    exit_reason, order_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_data.get('timestamp', datetime.now().isoformat()),
                trade_data.get('symbol'),
                trade_data.get('strike'),
                trade_data.get('option_type'),
                trade_data.get('entry_price'),
                trade_data.get('exit_price'),
                trade_data.get('quantity'),
                trade_data.get('side'),
                trade_data.get('status'),
                trade_data.get('pnl'),
                trade_data.get('pnl_percentage'),
                trade_data.get('exit_reason'),
                trade_data.get('order_id')
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Trade saved: {trade_data.get('symbol')} {trade_data.get('strike')}")
            
        except Exception as e:
            logger.error(f"Error saving trade: {str(e)}")
    
    def get_trade_history(self, limit=100):
        """
        Get trade history from database
        
        Args:
            limit: Number of trades to retrieve
            
        Returns:
            list: List of trades
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM trades 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            columns = [description[0] for description in cursor.description]
            trades = []
            
            for row in cursor.fetchall():
                trade = dict(zip(columns, row))
                trades.append(trade)
            
            conn.close()
            return trades
            
        except Exception as e:
            logger.error(f"Error fetching trade history: {str(e)}")
            return []
