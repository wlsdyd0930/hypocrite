from .client import get_ibm_client
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def verify_ibm_sentence(original_sentence, solution):
    sentence_result = {}
    # Instantiates a client
    try:
        client = get_ibm_client()
        sentence_score = client.analyze(
            language='en',
            text=original_sentence,
            features=Features(sentiment=SentimentOptions())).get_result()['sentiment']['document']
        print(sentence_score)
        if sentence_score['label'] == 'neutral':
            sentence_result['check'] = False
        elif sentence_score['label'] != solution:
            sentence_result['check'] = False
        else:
            sentence_result['sentence'] = original_sentence
            sentence_result["sentiment"] = sentence_score["label"]
            sentence_result['sentiment_score'] = sentence_score["score"]
            sentence_result['check'] = True
    except:
        print("Error")
        sentence_result['check'] = False
    return sentence_result