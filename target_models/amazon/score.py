import boto3
import os
import pandas as pd
from unicode import change_to_another_unicode

def get_tokenization_score(target_model, original_sentence, original_sentiment, target_result, type):

    if target_result is None:
        if original_sentiment == 'positive':
            original_sentiment = 'Positive'
        elif original_sentiment == 'negative':
            original_sentiment = 'Negative'
    else:
        if target_result == 'positive':
            target_result = 'Positive'
        elif target_result == 'negative':
            target_result = 'Negative'
        elif target_result == 'neutral':
            target_result = 'Neutral'
        elif target_result == 'mixed':
            target_result = 'Mixed'

    # Tokenization
    if type == 'word':
        original_tokenization_list = list(set(original_sentence.split(" ")))
    elif type == 'sentence':
        original_tokenization_list = list(original_sentence.split("."))
        original_tokenization_list = list(filter(None, original_tokenization_list))  # 빈 리스트 제거
        for index in range(len(original_tokenization_list)):
            original_tokenization_list[index] = original_tokenization_list[index].strip()
    elif type == 'paragraph':
        original_tokenization_list = [original_sentence]

    tokenization_list = []

    for original_tokenization in original_tokenization_list:
        result = {}
        comprehend = boto3.client('comprehend')

        if type == 'word':
            file = "target_models/" + target_model + "/" + target_model + "_word_dict.csv"
            if os.path.isfile(file):
                df = pd.read_csv(file)
            else:
                df = pd.DataFrame(columns = ['original_word', 'Positive', 'Neutral', 'Negative', 'Mixed'])

            word_df = df.loc[df['original_word'] == original_tokenization]
            if word_df.empty:
                result["original"] = original_tokenization
                result["original_score"] = comprehend.detect_sentiment(Text=original_tokenization, LanguageCode='en')["SentimentScore"]
                word_dict = {
                    'original_word': original_tokenization,
                    'Positive': result["original_score"]["Positive"],
                    'Neutral': result["original_score"]["Neutral"],
                    'Negative': result["original_score"]["Negative"],
                    'Mixed': result["original_score"]["Mixed"]
                }
                df = df.append(word_dict, ignore_index=True)
            else:
                result["original"] = word_df['original_word'].values[0]
                result["original_score"] = {
                    'Positive': float(word_df['Positive'].values[0]),
                    'Neutral': float(word_df['Neutral'].values[0]),
                    'Negative': float(word_df['Negative'].values[0]),
                    'Mixed': float(word_df['Mixed'].values[0])
                }
            attack_word = ""
            for character in result["original"]:
                letter = change_to_another_unicode(character)
                attack_word += letter
            result["substitution"] = attack_word
            df.to_csv(file, index=False)
        else:
            result["original"] = original_tokenization
            result["original_score"] = comprehend.detect_sentiment(Text=original_tokenization, LanguageCode='en')[
                "SentimentScore"]
            attack_word = ""
            for character in result["original"]:
                letter = change_to_another_unicode(character)
                attack_word += letter
            result["substitution"] = attack_word

        target_check = False
        if target_result is None:
            if original_sentiment == 'Positive':
                if min(result["original_score"], key=result["original_score"].get) != 'Positive':
                    target_check = True
            elif original_sentiment == 'Negative':
                if min(result["original_score"], key=result["original_score"].get) != 'Negative':
                    target_check = True
        else:
            if target_result != 'Neutral':
                if max(result["original_score"], key=result["original_score"].get) != target_result:
                    target_check = True
            else:
                target_check = True
        if target_check:
            tokenization_list.append(result)

    ############# Sort #####################
    if target_result is None:
        tokenization_list = sorted(tokenization_list, key=lambda tokenization_list: (
            tokenization_list["original_score"][original_sentiment]), reverse=True)
    else:
        tokenization_list = sorted(tokenization_list,
                            key=lambda tokenization_list: (tokenization_list["original_score"][target_result]),
                            reverse=False)

    return tokenization_list