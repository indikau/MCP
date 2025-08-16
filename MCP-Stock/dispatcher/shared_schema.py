from datetime import datetime

def format_output(source, symbol, sentiment_score, headline_count, trend, confidence):
    return {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "symbol": symbol,
        "sentiment_score": sentiment_score,
        "headline_count": headline_count,
        "trend": trend,
        "confidence": confidence
    }

def validate_schema(entry: dict) -> bool:
    required_keys = [
        "timestamp", "source", "symbol", 
        "sentiment_score", "headline_count", 
        "trend", "confidence"
    ]
    
    # Check for missing keys
    for key in required_keys:
        if key not in entry:
            print(f"❌ Missing key: {key}")
            return False
    
    # Basic type checks (optional but helpful)
    if not isinstance(entry["timestamp"], str): return False
    if not isinstance(entry["source"], str): return False
    if not isinstance(entry["symbol"], str): return False
    if not isinstance(entry["sentiment_score"], (float, int)): return False
    if not isinstance(entry["headline_count"], int): return False
    if not isinstance(entry["trend"], str): return False
    if not isinstance(entry["confidence"], (float, int)): return False
    
    return True