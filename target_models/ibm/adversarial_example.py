from pprint import pprint
from .score import get_tokenization_score
from .client import get_ibm_client
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def make_ibm_adversarial_example(result, score_list, target_result):
    client = get_ibm_client()

    for index, score in enumerate(score_list):
        temp_attack_sentence = result["attack_sentence"].replace(score["original"],
                                                                 score["substitution"])
        new_attack_result = client.analyze(
            language='en',
            text=temp_attack_sentence,
            features=Features(sentiment=SentimentOptions())).get_result()['sentiment']['document']

        if target_result is None:
            if new_attack_result["label"] != result["original_sentiment"]:
                result["attack_sentence"] = temp_attack_sentence
                result["attack_sentiment_score"] = new_attack_result['score']
                result["attack_sentiment"] = new_attack_result["label"]
                result['success_check'] = True
                break

            if result['original_sentiment'] == 'positive':
                if result["attack_sentiment_score"] >= new_attack_result['score']:
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result['score']
                    result["attack_sentiment"] = new_attack_result["label"]
            elif result['original_sentiment'] == 'negative':
                if result["attack_sentiment_score"] <= new_attack_result['score']:
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result['score']
                    result["attack_sentiment"] = new_attack_result["label"]
        else:

            if new_attack_result["label"] == target_result:
                result["attack_sentence"] = temp_attack_sentence
                result["attack_sentiment_score"] = new_attack_result['score']
                result["attack_sentiment"] = new_attack_result["label"]
                result['success_check'] = True
                break

            if target_result == 'positive':
                if result["attack_sentiment_score"] <= new_attack_result['score']:
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result['score']
                    result["attack_sentiment"] = new_attack_result["label"]
            elif target_result == 'negative':
                if result["attack_sentiment_score"] >= new_attack_result['score']:
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result['score']
                    result["attack_sentiment"] = new_attack_result["label"]
            elif target_result == 'neutral':
                if abs(result["attack_sentiment_score"]) >= abs(new_attack_result['score']):
                    result["attack_sentence"] = temp_attack_sentence
                    result["attack_sentiment_score"] = new_attack_result['score']
                    result["attack_sentiment"] = new_attack_result["label"]
            else:
                print('Error')

def get_ibm_adversarial_example(target_model, sentence_result, target_result):

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
        ############################## Unit ####################################################
        score_list = get_tokenization_score(target_model, result['attack_sentence'], result['original_sentiment'], target_result, type)
        make_ibm_adversarial_example(result, score_list, target_result)

        if result['success_check']:
            break

    return result