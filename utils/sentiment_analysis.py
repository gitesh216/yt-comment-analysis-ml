from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_comments(comments):
    results = []
    for comment in comments:
        scores = analyzer.polarity_scores(comment)
        sentiment = 'Neutral'
        if scores['compound'] >= 0.05:
            sentiment = 'Positive'
        elif scores['compound'] <= -0.05:
            sentiment = 'Negative'
        
        results.append({
            'comment': comment,
            'sentiment': sentiment,
            'scores': scores
        })
    return results
