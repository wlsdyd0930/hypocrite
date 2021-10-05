from pprint import pprint
from .score import get_tokenization_score
from .client import get_microsoft_client

def make_microsoft_non_targeted_adversarial_example(result, score_list):
    client = get_microsoft_client()
    for index, score in enumerate(score_list):
        temp_attack_sentence = result["attack_sentence"].replace(score["original"],
                                                                 score["substitution"])

        temp_new_attack_result = client.analyze_sentiment(documents=[temp_attack_sentence], show_opinion_mining=True)[0]
        new_attack_result = {}
        new_attack_result['sentiment_score'] = {
            'positive': temp_new_attack_result.confidence_scores.positive,
            'neutral': temp_new_attack_result.confidence_scores.neutral,
            'negative': temp_new_attack_result.confidence_scores.negative,
        }

        new_attack_result["Sentiment"] = temp_new_attack_result.sentiment

        if new_attack_result["Sentiment"] != result["original_sentiment"]:
            result["attack_sentence"] = temp_attack_sentence
            result["attack_sentiment_score"] = new_attack_result['sentiment_score']
            result["attack_sentiment"] = new_attack_result["Sentiment"]
            result['success_check'] = True
            break

        if result["attack_sentiment_score"][result["original_sentiment"]] >= new_attack_result['sentiment_score'][
            result["original_sentiment"]]:  # 공격이 성공하면
            result["attack_sentence"] = temp_attack_sentence
            result["attack_sentiment_score"] = new_attack_result['sentiment_score']
            result["attack_sentiment"] = new_attack_result["Sentiment"]

def make_microsoft_targeted_adversarial_example(result, score_list, target_result):
    client = get_microsoft_client()
    for index, score in enumerate(score_list):
        temp_attack_sentence = result["attack_sentence"].replace(score["original"],
                                                                 score["substitution"])
        temp_new_attack_result = client.analyze_sentiment(documents=[temp_attack_sentence], show_opinion_mining=True)[0]

        new_attack_result = {}
        new_attack_result['sentiment_score'] = {
            'positive': temp_new_attack_result.confidence_scores.positive,
            'neutral': temp_new_attack_result.confidence_scores.neutral,
            'negative': temp_new_attack_result.confidence_scores.negative,
        }

        new_attack_result["Sentiment"] = temp_new_attack_result.sentiment

        if new_attack_result["Sentiment"] == target_result:
            result["attack_sentence"] = temp_attack_sentence
            result["attack_sentiment_score"] = new_attack_result['sentiment_score']
            result["attack_sentiment"] = new_attack_result["Sentiment"]
            result['success_check'] = True
            break

        if target_result == 'mixed':
            max_diff = max(new_attack_result["sentiment_score"].values()) - max(
                result["attack_sentiment_score"].values())
            neutral_diff = new_attack_result["sentiment_score"]['neutral'] - result["attack_sentiment_score"]['neutral']

            if max_diff <= 0 and (abs(neutral_diff) <= abs(max_diff)):
                result["attack_sentence"] = temp_attack_sentence
                result["attack_sentiment_score"] = new_attack_result['sentiment_score']
                result["attack_sentiment"] = new_attack_result["Sentiment"]
        else:
            target_diff = new_attack_result["sentiment_score"][target_result] - result["attack_sentiment_score"][
                target_result]
            max_diff = max(new_attack_result["sentiment_score"].values()) - max(
                result["attack_sentiment_score"].values())

            if (target_diff >= 0) and (target_diff >= max_diff):
                result["attack_sentence"] = temp_attack_sentence
                result["attack_sentiment_score"] = new_attack_result["sentiment_score"]
                result["attack_sentiment"] = new_attack_result["Sentiment"]

def get_microsoft_adversarial_example(target_model, sentence_result, target_result):
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
        ############################## Word Unit ####################################################
        score_list = get_tokenization_score(target_model, result['attack_sentence'], result['original_sentiment'], target_result, type)
        if target_result is None:
            make_microsoft_non_targeted_adversarial_example(result, score_list)
        else:
            make_microsoft_targeted_adversarial_example(result, score_list, target_result)

        if result['success_check']:
            break

    return result