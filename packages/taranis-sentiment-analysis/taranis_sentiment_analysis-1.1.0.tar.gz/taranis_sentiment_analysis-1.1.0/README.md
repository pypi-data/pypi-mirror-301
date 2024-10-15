# Taranis AI Sentiment Analysis

This project integrates sentiment analysis into [Taranis AI](https://github.com/taranis-ai/taranis-ai), allowing for the classification of news items as **positive**, **negative**, or **neutral** using transformer models. The API intelligently chooses the appropriate model based on the text length, utilizing **XLM-RoBERTa** for shorter texts and **Longformer** for longer texts.

## Features
- **Multi-language Support** with XLM-RoBERTa and Longformer.
- **Pre-trained Models** for high-accuracy sentiment classification.
- **Flask API** for external calls to the sentiment analysis.

## Setup

### Prerequisites
- Python 3.8+

### Installation
To install dependencies:
```bash
pip install -r requirements.txt
```

### Running the API
To start the Flask API:

```bash
python -m sentiment_analysis.api.api_multimodel
```
By default, the API runs at http://127.0.0.1:5003/.

### Example API Call
To test the API with a POST request, use curl:

```bash
curl -X POST http://127.0.0.1:5003/analyze_sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "This is an example sentence to analyze sentiment."}'
```
### Example Response
```json
{
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.94
  }
}
```

## License
EUROPEAN UNION PUBLIC LICENCE v. 1.2

