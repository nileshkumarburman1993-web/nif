"""
15-Minute Candle Prediction Logic
Predicts next candle direction using technical analysis
"""

def identify_candle_pattern(open_price, high, low, close, prev_open=None, prev_close=None):
    """
    Identify candlestick pattern
    Returns: (pattern_name, is_bullish, strength)
    """
    body = abs(close - open_price)
    total_range = high - low
    upper_shadow = high - max(open_price, close)
    lower_shadow = min(open_price, close) - low
    
    # Avoid division by zero
    if total_range == 0:
        return ("Doji", None, 0)
    
    body_to_range = body / total_range if total_range > 0 else 0
    
    # Pattern detection
    
    # 1. DOJI - Very small body
    if body < total_range * 0.1:
        return ("Doji", None, 2)  # Neutral, medium strength
    
    # 2. HAMMER - Long lower shadow, small body at top
    if (lower_shadow > body * 2 and 
        upper_shadow < body * 0.3 and
        body_to_range < 0.3):
        return ("Hammer", True, 3)  # Bullish, strong
    
    # 3. INVERTED HAMMER - Long upper shadow, small body at bottom
    if (upper_shadow > body * 2 and 
        lower_shadow < body * 0.3 and
        body_to_range < 0.3):
        return ("Inverted Hammer", True, 2)  # Bullish, medium
    
    # 4. SHOOTING STAR - Long upper shadow, small body at bottom
    if (upper_shadow > body * 2 and 
        lower_shadow < body * 0.5 and
        close < open_price):
        return ("Shooting Star", False, 3)  # Bearish, strong
    
    # 5. HANGING MAN - Long lower shadow, small body at top, bearish context
    if (lower_shadow > body * 2 and 
        upper_shadow < body * 0.3 and
        close < open_price):
        return ("Hanging Man", False, 2)  # Bearish, medium
    
    # 6. MARUBOZU - Almost no shadows, strong body
    if body_to_range > 0.9:
        if close > open_price:
            return ("Bullish Marubozu", True, 4)  # Very strong bullish
        else:
            return ("Bearish Marubozu", False, 4)  # Very strong bearish
    
    # 7. SPINNING TOP - Small body, long shadows both sides
    if (body_to_range < 0.3 and 
        upper_shadow > body and 
        lower_shadow > body):
        return ("Spinning Top", None, 1)  # Neutral, weak
    
    # 8. BULLISH/BEARISH ENGULFING (needs previous candle)
    if prev_open is not None and prev_close is not None:
        prev_body = abs(prev_close - prev_open)
        
        # Bullish Engulfing
        if (prev_close < prev_open and  # Previous was bearish
            close > open_price and  # Current is bullish
            open_price < prev_close and  # Opens below prev close
            close > prev_open):  # Closes above prev open
            return ("Bullish Engulfing", True, 4)
        
        # Bearish Engulfing
        if (prev_close > prev_open and  # Previous was bullish
            close < open_price and  # Current is bearish
            open_price > prev_close and  # Opens above prev close
            close < prev_open):  # Closes below prev open
            return ("Bearish Engulfing", False, 4)
    
    # 9. Regular bullish/bearish candles
    if close > open_price:
        if body_to_range > 0.7:
            return ("Strong Bullish Candle", True, 3)
        else:
            return ("Bullish Candle", True, 2)
    else:
        if body_to_range > 0.7:
            return ("Strong Bearish Candle", False, 3)
        else:
            return ("Bearish Candle", False, 2)
    
    return ("Unknown", None, 0)


def predict_next_candle(candles, pcr, max_pain, current_price):
    """
    Predict next 15-min candle direction
    Returns: 'BULLISH', 'BEARISH', or 'NEUTRAL'
    """
    if not candles or len(candles) < 3:
        return {
            'direction': 'NEUTRAL',
            'confidence': 0,
            'reason': 'Insufficient candle data'
        }
    
    # Analyze last 3 candles
    last_candle = candles[-1]
    prev_candle = candles[-2]
    prev_prev = candles[-3] if len(candles) >= 3 else None
    
    # Extract OHLC (format: [timestamp, open, high, low, close, volume])
    try:
        last_open = float(last_candle[1])
        last_high = float(last_candle[2])
        last_low = float(last_candle[3])
        last_close = float(last_candle[4])
        last_volume = float(last_candle[5]) if len(last_candle) > 5 else 0
        
        prev_open = float(prev_candle[1])
        prev_close = float(prev_candle[4])
        
        # Calculate candle body and range
        last_body = abs(last_close - last_open)
        last_range = last_high - last_low
        last_upper_shadow = last_high - max(last_open, last_close)
        last_lower_shadow = min(last_open, last_close) - last_low
        
        # Identify current candle pattern
        current_pattern, is_bullish, pattern_strength = identify_candle_pattern(
            last_open, last_high, last_low, last_close, 
            prev_open, prev_close
        )
        
        # Bullish/Bearish signals
        bullish_signals = 0
        bearish_signals = 0
        
        # 1. Candle pattern analysis
        if is_bullish == True:
            bullish_signals += pattern_strength
        elif is_bullish == False:
            bearish_signals += pattern_strength
        else:  # Neutral pattern
            if last_close > last_open:
                bullish_signals += 1
            else:
                bearish_signals += 1
        
        # 2. Trend analysis (3 candles)
        if prev_prev:
            prev_prev_close = float(prev_prev[4])
            if last_close > prev_close > prev_prev_close:
                bullish_signals += 2  # Strong uptrend
            elif last_close < prev_close < prev_prev_close:
                bearish_signals += 2  # Strong downtrend
        
        # 3. PCR analysis
        if pcr < 0.7:  # Very bullish
            bullish_signals += 2
        elif pcr > 1.3:  # Very bearish
            bearish_signals += 2
        elif pcr < 1.0:  # Mildly bullish
            bullish_signals += 1
        elif pcr > 1.0:  # Mildly bearish
            bearish_signals += 1
        
        # 4. Price vs Max Pain
        distance_from_max_pain = current_price - max_pain
        if distance_from_max_pain < -100:  # Far below max pain
            bullish_signals += 1  # Likely to move up
        elif distance_from_max_pain > 100:  # Far above max pain
            bearish_signals += 1  # Likely to move down
        
        # 5. Volume analysis
        if len(candles) >= 5:
            avg_volume = sum(float(c[5]) if len(c) > 5 else 0 for c in candles[-5:]) / 5
            if last_volume > avg_volume * 1.2:  # High volume
                if last_close > last_open:
                    bullish_signals += 1
                else:
                    bearish_signals += 1
        
        # 6. Shadow analysis (candlestick patterns)
        if last_lower_shadow > last_body * 2 and last_upper_shadow < last_body * 0.5:
            bullish_signals += 1  # Hammer-like pattern
        elif last_upper_shadow > last_body * 2 and last_lower_shadow < last_body * 0.5:
            bearish_signals += 1  # Shooting star-like pattern
        
        # 7. Price momentum
        if last_close > prev_close:
            momentum = ((last_close - prev_close) / prev_close) * 100
            if momentum > 0.3:  # Strong momentum
                bullish_signals += 1
        else:
            momentum = ((prev_close - last_close) / prev_close) * 100
            if momentum > 0.3:
                bearish_signals += 1
        
        # Final decision
        total_signals = bullish_signals + bearish_signals
        confidence = 0
        direction = 'NEUTRAL'
        
        if bullish_signals > bearish_signals:
            direction = 'BULLISH'
            confidence = min(90, (bullish_signals / total_signals) * 100)
        elif bearish_signals > bullish_signals:
            direction = 'BEARISH'
            confidence = min(90, (bearish_signals / total_signals) * 100)
        else:
            direction = 'NEUTRAL'
            confidence = 50
        
        return {
            'direction': direction,
            'confidence': int(confidence),
            'last_close': last_close,
            'bullish_signals': bullish_signals,
            'bearish_signals': bearish_signals,
            'pattern': current_pattern,
            'pattern_strength': pattern_strength,
            'reason': f"{current_pattern} pattern detected - {bullish_signals} bullish vs {bearish_signals} bearish signals"
        }
        
    except Exception as e:
        print(f"Error in candle prediction: {e}")
        return {
            'direction': 'NEUTRAL',
            'confidence': 0,
            'reason': f'Analysis error: {str(e)}'
        }


def get_trading_recommendation(candle_prediction, pcr, max_pain, current_price):
    """
    Generate actionable trading recommendation
    """
    direction = candle_prediction['direction']
    confidence = candle_prediction['confidence']
    
    if direction == 'BULLISH' and confidence >= 60:
        # Recommend CALL buying
        entry = current_price
        target = current_price + 100
        sl = current_price - 50
        
        return {
            'action': 'BUY',
            'type': 'CALL',
            'entry': entry,
            'target': target,
            'sl': sl,
            'confidence': confidence,
            'reason': f"Next 15m candle predicted BULLISH ({confidence}%)"
        }
    
    elif direction == 'BEARISH' and confidence >= 60:
        # Recommend PUT buying
        entry = current_price
        target = current_price - 100
        sl = current_price + 50
        
        return {
            'action': 'BUY',
            'type': 'PUT',
            'entry': entry,
            'target': target,
            'sl': sl,
            'confidence': confidence,
            'reason': f"Next 15m candle predicted BEARISH ({confidence}%)"
        }
    
    else:
        return {
            'action': 'WAIT',
            'confidence': confidence,
            'reason': f"Low confidence ({confidence}%) or neutral market"
        }
