import os
import pandas as pd
from unicode import change_to_another_unicode
from .client import get_ibm_client
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_tokenization_score(target_model, original_sentence, original_sentiment, target_result, type):

    # Instantiates a client
    client = get_ibm_client()
    tokenization_list = []

    if type == 'word':
        original_tokenization_list = list(set(original_sentence.split(" ")))
    elif type == 'sentence':
        original_tokenization_list = list(original_sentence.split("."))
        original_tokenization_list = list(filter(None, original_tokenization_list))
        for index in range(len(original_tokenization_list)):
            original_tokenization_list[index] = original_tokenization_list[index].strip()
    elif type == 'paragraph':
        original_tokenization_list = [original_sentence]

    if target_result != 'neutral':
        targets = client.analyze(
            language='en',
            text=original_sentence,
            features=Features(sentiment=SentimentOptions(targets=original_tokenization_list))).get_result()['sentiment']['targets']
        for target in targets:
            result = {}
            result["original"] = target['text']
            result["original_score"] = target['score']
            target_check = False
            if target_result is None:
                if original_sentiment == 'positive':
                    if result["original_score"] >= 0:
                        target_check = True
                elif original_sentiment == 'negative':
                    if result["original_score"] <= 0:
                        target_check = True
            else:
                if target_result == 'positive':
                    if result["original_score"] <= 0:
                        target_check = True
                elif target_result == 'neutral':
                    target_check = True
                elif target_result == 'negative':
                    if result["original_score"] >= 0:
                        target_check = True
                else:
                    print('Error')

            if target_check:
                attack_word = ""
                for character in result["original"]:
                    letter = change_to_another_unicode(character)
                    attack_word += letter
                result["substitution"] = attack_word
                tokenization_list.append(result)

    else:
        for original_tokenization in original_tokenization_list:
            result = {}
            if type == 'word':
                file = "target_models/" + target_model + "/" + target_model + "_word_dict.csv"
                if os.path.isfile(file):
                    df = pd.read_csv(file)
                else:
                    df = pd.DataFrame(columns=['original_word', 'score'])

                word_df = df.loc[df['original_word'] == original_tokenization]
                if word_df.empty:
                    target = client.analyze(
                        language='en',
                        text=original_tokenization,
                        features=Features(sentiment=SentimentOptions())).get_result()['sentiment']['document']

                    result["original"] = original_tokenization
                    result["original_score"] = target["score"]

                    word_dict = {
                        'original_word': original_tokenization,
                        'score': result["original_score"]
                    }
                    df = df.append(word_dict, ignore_index=True)
                else:
                    result["original"] = word_df['original_word'].values[0]
                    result["original_score"] = float(word_df['score'].values[0])
                attack_word = ""
                for character in result["original"]:
                    letter = change_to_another_unicode(character)
                    attack_word += letter
                result["substitution"] = attack_word
                df.to_csv(file, index=False)
            else:
                target = client.analyze(
                    language='en',
                    text=original_tokenization,
                    features=Features(sentiment=SentimentOptions())).get_result()['sentiment']['document']

                result["original"] = original_tokenization
                result["original_score"] = target["score"]
                attack_word = ""
                for character in result["original"]:
                    letter = change_to_another_unicode(character)
                    attack_word += letter
                result["substitution"] = attack_word

            tokenization_list.append(result)


    if original_sentiment == 'positive':
        tokenization_list = sorted(tokenization_list,
                            key=lambda tokenization_list: (tokenization_list["original_score"]),
                            reverse=True)
    elif original_sentiment == 'negative':
        tokenization_list = sorted(tokenization_list,
                            key=lambda tokenization_list: (tokenization_list["original_score"]),
                            reverse=False)
    return tokenization_list