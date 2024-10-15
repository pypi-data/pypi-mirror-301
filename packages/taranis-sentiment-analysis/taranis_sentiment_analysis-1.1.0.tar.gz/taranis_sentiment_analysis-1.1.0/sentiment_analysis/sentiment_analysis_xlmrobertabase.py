from transformers import pipeline

# Load pre trained XLM-RoBERTa model for sentiment-analysis
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

# Label mapping for the sentiment output
label_mapping = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using the XLM-RoBERTa model.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary with the raw output of the model.
    """
    result = sentiment_pipeline(text)[0]    
    return result 


def categorize_text(sentiment_result, positive_threshold=0.5, negative_threshold=0.5):
    """
    Categorize the sentiment as positive, negative, or neutral based on thresholds.

    Args:
        sentiment_result (dict): The result from the sentiment analysis containing label and score.
        positive_threshold (float): The threshold above which the sentiment is considered positive.
        negative_threshold (float): The threshold below which the sentiment is considered negative.

    Returns:
        str: The category of the sentiment ('positive', 'negative', 'neutral').
    """
    label = sentiment_result['label']
    score = sentiment_result['score']
    
    if label == 'LABEL_2' and score >= positive_threshold:
        return "positive"
    elif label == 'LABEL_0' and score >= negative_threshold:
        return "negative"
    else:
        return "neutral"

