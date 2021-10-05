from .client import get_microsoft_client

def verify_microsoft_sentence(original_sentence, solution):
    sentence_result = {}
    # Instantiates a client
    try:
        client = get_microsoft_client()
        sentence_score = client.analyze_sentiment(documents=[original_sentence], show_opinion_mining=True, language="en")[0]
        sentence_result['sentiment_score'] = {
            'positive': sentence_score.confidence_scores.positive,
            'neutral': sentence_score.confidence_scores.neutral,
            'negative': sentence_score.confidence_scores.negative,
        }
        sentence_result["sentiment"] = sentence_score.sentiment
        print(sentence_result)
        if sentence_result["sentiment"] == 'neutral' or sentence_result["sentiment"] == 'mixed':
            sentence_result['check'] = False
        elif sentence_result["sentiment"] == 'positive' and solution == "negative":
            sentence_result['check'] = False
        elif sentence_result["sentiment"] == 'negative' and solution == "positive":
            sentence_result['check'] = False
        else:
            sentence_result['sentence'] = original_sentence
            sentence_result['check'] = True
    except:
        print("Error")
        sentence_result['check'] = False
    return sentence_result