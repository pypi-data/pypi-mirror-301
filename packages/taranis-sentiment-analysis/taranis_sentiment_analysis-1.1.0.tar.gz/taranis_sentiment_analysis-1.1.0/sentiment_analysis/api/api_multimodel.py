from flask import Flask, request, jsonify
from sentiment_analysis.sentiment_analysis_multimodel import analyze_sentiment

app = Flask(__name__)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_text():
    """
    Endpoint to analyze the sentiment of the given text using either XLM-RoBERTa or Longformer, depending on text length.
    Returns:
        JSON: A JSON response with the sentiment result and category.
    """
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        sentiment_result = analyze_sentiment(text)
        
        response = {
            "label": sentiment_result["label"],
            "score": sentiment_result["score"]
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"Failed to analyze sentiment: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
