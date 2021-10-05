import pandas as pd
import os
from pprint import pprint

def wirte_result(filename, result_report):

    df = pd.DataFrame(result_report, index=[0])
    df.to_csv(filename, index=False)
    print("\n")
    print(result_report)

def wirte_detail_result(filename, result):

    print("\n============================ Attacked Sentiment Result ================================")
    pprint(result)
    print("=======================================================================================\n")
    print("original_sentence:", result["original_sentence"])
    print("attack_sentence:", result["attack_sentence"])

    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['original_sentence', 'attack_sentence', 'original_sentiment', 'attack_sentiment',
                                   'success(True)/failed(False)', 'perturbed_ratio'])

    result_df = df.loc[df['original_sentence'] == result["original_sentence"]]

    if result_df.empty:
        word_dict = {
            'original_sentence': result["original_sentence"],
            'attack_sentence': result["attack_sentence"],
            'original_sentiment': result["original_sentiment"],
            'attack_sentiment': result["attack_sentiment"],
            'success(True)/failed(False)': result['success_check'],
            'perturbed_ratio': result['perturbed_ratio']
        }
        df = df.append(word_dict, ignore_index=True)
        df.to_csv(filename, index=False)