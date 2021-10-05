import os
import pandas as pd
from unicode import change_to_another_unicode
from .client import get_microsoft_client

def get_tokenization_score(target_model, original_sentence, original_sentiment, target_result, type):

    client = get_microsoft_client()

    # Tokenization
    if type == 'word':
        original_tokenization_list = list(set(original_sentence.split(" ")))
    elif type == 'sentence':
        response = client.analyze_sentiment(documents=[original_sentence], show_opinion_mining=True)[0]
        original_tokenization_list = response.sentences
    elif type == 'paragraph':
        original_tokenization_list = [original_sentence]

    tokenization_list = []

    for original_tokenization in original_tokenization_list:
        result = {}
        if type == 'word':
            file = "target_models/" + target_model + "/" + target_model + "_word_dict.csv"
            if os.path.isfile(file):
                df = pd.read_csv(file)
            else:
                df = pd.DataFrame(columns = ['original_word', 'positive', 'neutral', 'negative'])

            word_df = df.loc[df['original_word'] == original_tokenization]
            try:
                if word_df.empty:
                    result["original"] = original_tokenization
                    response = client.analyze_sentiment(documents=[original_tokenization], show_opinion_mining=True)[0].confidence_scores

                    result["original_score"] = {
                        'positive': response.positive,
                        'neutral': response.neutral,
                        'negative': response.negative,
                    }
                    word_dict = {
                        'original_word': original_tokenization,
                        'positive': result["original_score"]['positive'],
                        'neutral': result["original_score"]['neutral'],
                        'negative': result["original_score"]['negative']
                    }
                    df = df.append(word_dict, ignore_index=True)
                else:
                    result["original"] = word_df['original_word'].values[0]
                    result["original_score"] = {
                        'positive': float(word_df['positive'].values[0]),
                        'neutral': float(word_df['neutral'].values[0]),
                        'negative': float(word_df['negative'].values[0])
                    }
                attack_word = ""
                for character in result["original"]:
                    letter = change_to_another_unicode(character)
                    attack_word += letter
                result["substitution"] = attack_word
                df.to_csv(file, index=False)
            except:
                print("Error")
        else:
            if type == 'sentence':
                result["original"] = original_tokenization.text
                result["original_score"] = {
                    'positive': original_tokenization.confidence_scores.positive,
                    'neutral': original_tokenization.confidence_scores.neutral,
                    'negative': original_tokenization.confidence_scores.negative,
                }
            elif type == 'paragraph':
                result["original"] = original_tokenization
                temp_score = client.analyze_sentiment(documents=[original_tokenization], show_opinion_mining=True)[
                    0].confidence_scores
                result["original_score"] = {
                    'positive': temp_score.positive,
                    'neutral': temp_score.neutral,
                    'negative': temp_score.negative,
                }
            attack_word = ""
            for character in result["original"]:
                letter = change_to_another_unicode(character)
                attack_word += letter
            result["substitution"] = attack_word

        target_check = False
        if target_result is None:
            if min(result["original_score"], key=result["original_score"].get) != original_sentiment:
                target_check = True
        else:
            if target_result != 'neutral':
                if max(result["original_score"], key=result["original_score"].get) != target_result:
                    target_check = True
            else:
                target_check = True
        if target_check:
            tokenization_list.append(result)

    if (target_result is None) or (target_result == 'mixed'):
        tokenization_list = sorted(tokenization_list, key=lambda tokenization_list: (
            tokenization_list["original_score"][original_sentiment]), reverse=True)
    else:
        tokenization_list = sorted(tokenization_list,
                                 key=lambda tokenization_list: (tokenization_list["original_score"][target_result]),
                                 reverse=False)
    return tokenization_list