from transformers import pipeline, LongformerForSequenceClassification, LongformerTokenizer


roberta_sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
longformer_tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")
longformer_model = LongformerForSequenceClassification.from_pretrained("allenai/longformer-base-4096")

label_mapping = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text. Select model based on text length.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary with the raw output of the model.
    """
    if not text or len(text.strip()) == 0:
        return {"error": "Empty text provided"}

    try:
        # Tokenize the text with RoBERTa tokenizer
        roberta_tokens = roberta_sentiment_pipeline.tokenizer(text)
        
        if len(roberta_tokens["input_ids"]) > 512:
            inputs = longformer_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = longformer_model(**inputs)
            logits = outputs.logits
            predicted_class_id = logits.argmax().item()
            
            # Map class ID to sentiment label
            sentiment = label_mapping[f"LABEL_{predicted_class_id}"]
            return {"label": sentiment, "score": logits.softmax(dim=1).max().item()}
        else:
            return roberta_sentiment_pipeline(text)[0]
    except Exception as e:
        return {"error": str(e)}

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
    
    if label == 'POSITIVE' and score >= positive_threshold:
        return "positive"
    elif label == 'NEGATIVE' and score <= negative_threshold:
        return "negative"
    else:
        return "neutral"
