"""
15-Minute Candle Prediction Logic
Predicts next candle direction using technical analysis
"""

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
        
        # Bullish/Bearish signals
        bullish_signals = 0
        bearish_signals = 0
        
        # 1. Candle pattern analysis
        if last_close > last_open:  # Green candle
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
            'reason': f"{bullish_signals} bullish vs {bearish_signals} bearish signals"
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
