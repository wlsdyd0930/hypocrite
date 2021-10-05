from pprint import pprint
from .score import get_tokenization_score
from google.cloud import language_v1

def make_google_adversarial_example(result, score_list, target_result):
    client = language_v1.LanguageServiceClient()

    for index, score in enumerate(score_list):
        temp_attack_sentence = result["attack_sentence"].replace(score["original"],
                                                                 score["substitution"])

        document = {"content": temp_attack_sentence, "type_": language_v1.Document.Type.PLAIN_TEXT,
                    "language": "en"}
        new_attack_result = client.analyze_sentiment(
            request={'document': document}).document_sentiment.score

        if target_result is None:

            if new_attack_result > 0:
                new_attack_sentiment = 'positive'
            elif new_attack_result == 0:
                new_attack_sentiment = 'neutral'
            elif new_attack_result < 0:
                new_attack_sentiment = 'negative'

            if new_attack_sentiment != result["original_sentiment"]:
                result["attack_sentence"] = temp_attack_sentence
                result["attack_sentiment_score"] = new_attack_result
                result["attack_sentiment"] = new_attack_sentiment
                result['success_check'] = True
                break

            if result['original_sentiment'] == 'positive':
                if result["attack_sentiment_score"] >= new_attack_result:
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result
                    result["attack_sentiment"] = new_attack_sentiment
            elif result['original_sentiment'] == 'negative':
                if result["attack_sentiment_score"] <= new_attack_result:
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result
                    result["attack_sentiment"] = new_attack_sentiment
        else:
            if new_attack_result > 0:
                new_attack_sentiment = 'positive'
            elif new_attack_result == 0:
                new_attack_sentiment = 'neutral'
            elif new_attack_result < 0:
                new_attack_sentiment = 'negative'

            if new_attack_sentiment == target_result:
                result["attack_sentence"] = temp_attack_sentence
                result["attack_sentiment_score"] = new_attack_result
                result["attack_sentiment"] = new_attack_sentiment
                result['success_check'] = True
                break

            if target_result == 'positive':
                if result["attack_sentiment_score"] <= new_attack_result:  # 공격이 성공하면
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result
                    result["attack_sentiment"] = new_attack_sentiment
            elif target_result == 'negative':
                if result["attack_sentiment_score"] >= new_attack_result:  # 공격이 성공하면
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result
                    result["attack_sentiment"] = new_attack_sentiment
            elif target_result == 'neutral':
                if abs(result["attack_sentiment_score"]) >= abs(new_attack_result):  # 공격이 성공하면
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result
                    result["attack_sentiment"] = new_attack_sentiment
            else:
                print('Error')

def get_google_adversarial_example(target_model, sentence_result, target_result):

    original_sentence = sentence_result['sentence'].replace("\n", "")

    result = {
        "original_sentence": original_sentence,
        "attack_sentence": original_sentence,
        "original_sentiment": sentence_result['sentiment'],
        "attack_sentiment": sentence_result['sentiment'],
        "original_sentiment_score": sentence_result['sentiment_score'],
        "attack_sentiment_score": sentence_result['sentiment_score'],
        "success_check": False
    }

    print("\n============================[{0}] Original Sentiment Result ================================".format(target_model))
    pprint(result)
    print("=======================================================================================\n")

    types = ['word', 'sentence', 'paragraph']

    for type in types:
        ############################### Unit ####################################################
        score_list = get_tokenization_score(target_model, result['attack_sentence'], result['original_sentiment'], target_result, type)
        make_google_adversarial_example(result, score_list, target_result)

        if result['success_check']:
            break

    return result