def analyze_sentiment(text: str):
    text = text.lower()

    if "keren" in text or "bagus" in text:
        sentiment = "positive"
    elif "jelek" in text or "lambat" in text:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "confidence": 0.99
    }
