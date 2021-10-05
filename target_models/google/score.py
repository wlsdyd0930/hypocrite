import os
import pandas as pd
from google.cloud import language_v1
from unicode import change_to_another_unicode

def get_tokenization_score(target_model, original_sentence, original_sentiment, target_result, type):
    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    if type == 'word':
        original_tokenization_list = list(set(original_sentence.split(" ")))
    elif type == 'sentence':
        document = {"content": original_sentence, "type_": language_v1.Document.Type.PLAIN_TEXT,
                    "language": "en"}
        original_tokenization_list = client.analyze_sentiment(request={'document': document}).sentences
    elif type == 'paragraph':
        document = {"content": original_sentence, "type_": language_v1.Document.Type.PLAIN_TEXT,
                    "language": "en"}
        original_tokenization_list = client.analyze_sentiment(request={'document': document}).sentences

    tokenization_list = []

    for original_tokenization in original_tokenization_list:
        result = {}
        if type == 'word':
            file = "target_models/" + target_model + "/" + target_model + "_word_dict.csv"
            if os.path.isfile(file):
                df = pd.read_csv(file)
            else:
                df = pd.DataFrame(columns = ['original_word', 'score'])

            word_df = df.loc[df['original_word'] == original_tokenization]
            if word_df.empty:
                result["original"] = original_tokenization
                document = {"content": original_tokenization, "type_": language_v1.Document.Type.PLAIN_TEXT,
                            "language": "en"}
                result["original_score"] = client.analyze_sentiment(request={'document': document}).document_sentiment.score

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
            result["original"] = original_tokenization.text.content
            result["original_score"] = original_tokenization.sentiment.score
            attack_word = ""
            for character in result["original"]:
                letter = change_to_another_unicode(character)
                attack_word += letter
            result["substitution"] = attack_word

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
            tokenization_list.append(result)

    # Sort
    if original_sentiment == 'positive':
        tokenization_list = sorted(tokenization_list,
                            key=lambda tokenization_list: (tokenization_list["original_score"]),
                            reverse=True)
    elif original_sentiment == 'negative':
        tokenization_list = sorted(tokenization_list,
                            key=lambda tokenization_list: (tokenization_list["original_score"]),
                            reverse=False)

    return tokenization_list