"""
Main Flask Application for Trading Automation
Handles API routes and coordinates trading operations with background updates
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from strategy import TradingStrategy
import schedule
import threading
import time
import logging
import os

# Initialize Flask app
app = Flask(__name__, 
            static_folder='../frontend',
            template_folder='../frontend')
CORS(app)

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize strategy
strategy = TradingStrategy()
market_data = {}
trading_active = False


def update_market_data():
    """Background task to update data every 1 minute"""
    global market_data
    while True:
        try:
            if trading_active:
                market_data = strategy.analyze_market("BANKNIFTY")
                if market_data:
                    logger.info(f"📊 Updated - PCR: {market_data.get('pcr')}, "
                              f"Max Pain: {market_data.get('max_pain')}, "
                              f"Signal: {market_data.get('signal', {}).get('action')}")
                else:
                    logger.warning("Failed to update market data")
            time.sleep(60)  # Update every minute
        except Exception as e:
            logger.error(f"Error in update_market_data: {str(e)}")
            time.sleep(60)


@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    """Login to Angel One API"""
    try:
        if strategy.angel.is_logged_in():
            logger.info("Already logged in to Angel One")
            return jsonify({
                'success': True,
                'message': 'Already logged in',
                'user': strategy.angel.get_profile()
            })
        
        if strategy.angel.login():
            logger.info("Successfully logged in to Angel One")
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': strategy.angel.get_profile()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Login failed'
            }), 401
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/market-data')
def get_market_data():
    """Get current market data and signals"""
    return jsonify(market_data if market_data else {
        'error': 'No data available',
        'signal': {'action': 'WAIT'}
    })


@app.route('/api/start-trading', methods=['POST'])
def start_trading():
    """Start automated trading"""
    global trading_active
    
    if not strategy.angel.is_logged_in():
        return jsonify({
            'success': False,
            'message': 'Please login first'
        }), 401
    
    try:
        data = request.json if request.json else {}
        symbol = data.get('symbol', 'BANKNIFTY')
        
        trading_active = True
        
        # Immediate first update
        global market_data
        market_data = strategy.analyze_market(symbol)
        
        logger.info(f"Started trading for {symbol}")
        return jsonify({
            'success': True,
            'message': f'Trading started for {symbol}',
            'data': market_data
        })
        
    except Exception as e:
        logger.error(f"Error starting trading: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/stop-trading', methods=['POST'])
def stop_trading():
    """Stop automated trading"""
    global trading_active
    
    try:
        trading_active = False
        
        logger.info("Trading stopped")
        return jsonify({
            'success': True,
            'message': 'Trading stopped'
        })
        
    except Exception as e:
        logger.error(f"Error stopping trading: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/execute-trade', methods=['POST'])
def execute_trade():
    """Execute trade based on current signal"""
    try:
        signal = market_data.get('signal', {})
        
        if signal.get('action') == 'WAIT':
            return jsonify({
                'success': False,
                'message': 'No trading signal available'
            })
        
        result = strategy.execute_trade(signal)
        
        return jsonify({
            'success': True if result else False,
            'message': 'Trade executed' if result else 'Trade execution failed',
            'order': result
        })
        
    except Exception as e:
        logger.error(f"Error executing trade: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/positions', methods=['GET'])
def get_positions():
    """Get current positions"""
    if not strategy.angel.is_logged_in():
        return jsonify({
            'success': False,
            'message': 'Please login first'
        }), 401
    
    try:
        positions = strategy.angel.get_positions()
        return jsonify({
            'success': True,
            'positions': positions
        })
        
    except Exception as e:
        logger.error(f"Error fetching positions: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/option-chain/<symbol>', methods=['GET'])
def get_option_chain(symbol):
    """Get option chain data"""
    try:
        df = strategy.oc.get_nse_data(symbol)
        
        if df is not None:
            # Calculate metrics
            pcr = strategy.oc.calculate_pcr(df)
            max_pain = strategy.oc.get_max_pain(df)
            heavy_call, heavy_put = strategy.oc.get_heavy_strikes(df)
            
            return jsonify({
                'success': True,
                'data': {
                    'pcr': pcr,
                    'max_pain': max_pain,
                    'heavy_call': heavy_call,
                    'heavy_put': heavy_put,
                    'options': df.to_dict('records')[:20]  # Send top 20 strikes
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to fetch option chain'
            }), 500
        
    except Exception as e:
        logger.error(f"Error fetching option chain: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/trade-history', methods=['GET'])
def get_trade_history():
    """Get trade history from database"""
    try:
        history = strategy.get_trade_history()
        return jsonify({
            'success': True,
            'trades': history
        })
            
    except Exception as e:
        logger.error(f"Error fetching trade history: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


if __name__ == '__main__':
    # Ensure database directory exists
    os.makedirs('../database', exist_ok=True)
    
    # Start background data updater thread
    logger.info("Starting background market data updater...")
    thread = threading.Thread(target=update_market_data, daemon=True)
    thread.start()
    
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    logger.info(f"Starting Flask server on http://0.0.0.0:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)
