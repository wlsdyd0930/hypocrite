import boto3
from pprint import pprint
from .score import get_tokenization_score

def make_amazon_non_targeted_adversarial_example(result, score_list):
    comprehend = boto3.client('comprehend')

    if result["original_sentiment"] == 'positive':
        original_sentiment = 'Positive'
    elif result["original_sentiment"] == 'negative':
        original_sentiment = 'Negative'

    for index, score in enumerate(score_list):
        temp_attack_sentence = result["attack_sentence"].replace(score["original"],
                                                                 score["substitution"])
        new_attack_result = comprehend.detect_sentiment(Text=temp_attack_sentence, LanguageCode='en')

        if new_attack_result["Sentiment"] == "POSITIVE":
            new_attack_result["Sentiment"] = "positive"
        elif new_attack_result["Sentiment"] == "NEGATIVE":
            new_attack_result["Sentiment"] = "negative"
        elif new_attack_result["Sentiment"] == "NEUTRAL":
            new_attack_result["Sentiment"] = "neutral"
        elif new_attack_result["Sentiment"] == "MIXED":
            new_attack_result["Sentiment"] = "mixed"

        if new_attack_result["Sentiment"] != result["original_sentiment"]:
            result["attack_sentence"] = temp_attack_sentence
            result["attack_sentiment_score"] = new_attack_result["SentimentScore"]
            result["attack_sentiment"] = new_attack_result["Sentiment"]
            result['success_check'] = True
            break

        if result["attack_sentiment_score"][original_sentiment] >= new_attack_result["SentimentScore"][original_sentiment]:
            result["attack_sentence"] = temp_attack_sentence
            result["attack_sentiment_score"] = new_attack_result["SentimentScore"]
            result["attack_sentiment"] = new_attack_result["Sentiment"]

def make_amazon_targeted_adversarial_example(result, score_list, target_result):
    comprehend = boto3.client('comprehend')

    if target_result == 'positive':
        temp_target_result = 'Positive'
    elif target_result == 'negative':
        temp_target_result = 'Negative'
    elif target_result == 'neutral':
        temp_target_result = 'Neutral'
    elif target_result == 'mixed':
        temp_target_result = 'Mixed'

    for index, score in enumerate(score_list):
        temp_attack_sentence = result["attack_sentence"].replace(score["original"],
                                                                 score["substitution"])
        new_attack_result = comprehend.detect_sentiment(Text=temp_attack_sentence, LanguageCode='en')

        if new_attack_result["Sentiment"] == "POSITIVE":
            new_attack_result["Sentiment"] = "positive"
        elif new_attack_result["Sentiment"] == "NEGATIVE":
            new_attack_result["Sentiment"] = "negative"
        elif new_attack_result["Sentiment"] == "NEUTRAL":
            new_attack_result["Sentiment"] = "neutral"
        elif new_attack_result["Sentiment"] == "MIXED":
            new_attack_result["Sentiment"] = "mixed"

        target_diff = new_attack_result["SentimentScore"][temp_target_result] - result["attack_sentiment_score"][
            temp_target_result]
        max_diff = max(new_attack_result["SentimentScore"].values()) - max(
            result["attack_sentiment_score"].values())

        if new_attack_result["Sentiment"] == target_result:
            result["attack_sentence"] = temp_attack_sentence
            result["attack_sentiment_score"] = new_attack_result["SentimentScore"]
            result["attack_sentiment"] = new_attack_result["Sentiment"]
            result['success_check'] = True
            break

        if (target_diff >= 0) and (target_diff >= max_diff):
            result["attack_sentence"] = temp_attack_sentence
            result["attack_sentiment_score"] = new_attack_result["SentimentScore"]
            result["attack_sentiment"] = new_attack_result["Sentiment"]

def get_amazon_adversarial_example(target_model, sentence_result, target_result, type):
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
        if target_result is None:
            make_amazon_non_targeted_adversarial_example(result, score_list)
        else:
            make_amazon_targeted_adversarial_example(result, score_list, target_result)

        if result['success_check']:
            break

    return result