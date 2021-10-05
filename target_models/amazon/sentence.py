import boto3

def verify_amazon_sentence(original_sentence, solution):
    sentence_result = {}
    comprehend = boto3.client('comprehend')
    try:
        sentence_score = comprehend.detect_sentiment(Text=original_sentence, LanguageCode='en')
        print(sentence_score)
        if sentence_score["Sentiment"] == "MIXED" or sentence_score["Sentiment"] == "NEUTRAL":
            sentence_result['check'] = False
        elif sentence_score["Sentiment"] == "POSITIVE" and solution == "negative":
            sentence_result['check'] = False
        elif sentence_score["Sentiment"] == "NEGATIVE" and solution == "positive":
            sentence_result['check'] = False
        else:
            sentence_result['sentence'] = original_sentence

            if sentence_score["Sentiment"] == "POSITIVE":
                sentence_result["sentiment"] = "positive"
            elif sentence_score["Sentiment"] == "NEGATIVE":
                sentence_result["sentiment"] = "negative"

            sentence_result['sentiment_score'] = sentence_score["SentimentScore"]
            sentence_result['check'] = True
    except:
        print("Error")
        sentence_result['check'] = False
    return sentence_result
