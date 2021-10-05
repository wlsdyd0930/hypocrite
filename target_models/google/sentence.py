from google.cloud import language_v1

def verify_google_sentence(original_sentence, solution):
    sentence_result = {}
    # Instantiates a client
    client = language_v1.LanguageServiceClient()
    try:
        document = {"content": original_sentence, "type_": language_v1.Document.Type.PLAIN_TEXT, "language": "en"}
        sentence_score = client.analyze_sentiment(request={'document': document}).document_sentiment.score
        print(sentence_score)
        if sentence_score == 0 :      # 0: Neutral
            sentence_result['check'] = False
        elif 0 < sentence_score and solution == "negative":
            sentence_result['check'] = False
        elif sentence_score < 0 and solution == "positive":
            sentence_result['check'] = False
        else:
            sentence_result['sentence'] = original_sentence

            if 0 < sentence_score:                      # 0 ~ 1: Positive
                sentence_result["sentiment"] = "positive"
            elif sentence_score < 0:                   # -1 ~ 0: Negative
                sentence_result["sentiment"] = "negative"

            sentence_result['sentiment_score'] = sentence_score

            sentence_result['check'] = True
    except:
        print("Error")
        sentence_result['check'] = False
    return sentence_result
