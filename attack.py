import random
from dataset import get_dataset
from target_models.amazon.adversarial_example import get_amazon_adversarial_example
from target_models.google.adversarial_example import get_google_adversarial_example
from target_models.ibm.adversarial_example import get_ibm_adversarial_example
from target_models.microsoft.adversarial_example import get_microsoft_adversarial_example
from target_models.amazon.sentence import verify_amazon_sentence
from target_models.google.sentence import verify_google_sentence
from target_models.ibm.sentence import verify_ibm_sentence
from target_models.microsoft.sentence import verify_microsoft_sentence
from result import wirte_result
from result import wirte_detail_result

def attack_model(config, sentence_result, result_report):
    target_result = config['target_result']

    if config['target_model'] == 'amazon':
        result = get_amazon_adversarial_example(config['target_model'], sentence_result, target_result, type)
    elif config['target_model'] == 'google':
        result = get_google_adversarial_example(config['target_model'], sentence_result, target_result)
    elif config['target_model'] == 'ibm':
        result = get_ibm_adversarial_example(config['target_model'], sentence_result, target_result)
    elif config['target_model'] == 'microsoft':
        result = get_microsoft_adversarial_example(config['target_model'], sentence_result, target_result)

    original_sentence_list = list(result['original_sentence'])
    attack_sentence_list = list(result['attack_sentence'])
    diff_char = 0
    for i in range(len(original_sentence_list)):
        if original_sentence_list[i] != attack_sentence_list[i]:
            diff_char += 1
    result['perturbed_ratio'] = round(diff_char/len(original_sentence_list)*100, 2)

    result_report["total_num"] += 1

    if result['success_check']:
        if result["original_sentiment"] == "positive":
            result_report["[positive] success_num"] += 1
        elif result["original_sentiment"] == "negative":
            result_report["[negative] success_num"] += 1
        result_report['avg_perturbed_ratio'] += result['perturbed_ratio']

    if not result['success_check']:
        if result["original_sentiment"] == "positive":
            result_report["[positive] failed_num"] += 1
        elif result["original_sentiment"] == "negative":
            result_report["[negative] failed_num"] += 1

    # results/amazon/[IMDB]positive_negative_result_result_1_1.csv
    filename = 'results/{0}/[{1}]{2}_{3}_detail_result_{4}.csv'.format(
        config['target_model'], config['dataset'], config['source'], config['target_result'], config['length'])
    wirte_detail_result(filename, result)

    return result_report

def start_attack(config):
    df = get_dataset(config['dataset'], config['length'], config['source'])

    result_report = {
        "total_num": 0,
        "avg_perturbed_ratio": 0,
        "[positive] success_num": 0,
        "[negative] success_num": 0,
        "[positive] failed_num": 0,
        "[negative] failed_num": 0
    }

    sentence_result_list = []
    index_list = []

    sentence_num = min([config['sentence_num'],len(df)])

    while len(index_list) < sentence_num:
        index = random.randrange(0, len(df))
        if index not in index_list:
            original_sentence = df['review'].values[index]
            solution = df['sentiment'].values[index]
            if config['target_model'] == 'amazon':
                sentence_result = verify_amazon_sentence(original_sentence, solution)
            elif config['target_model'] == 'google':
                sentence_result = verify_google_sentence(original_sentence, solution)
            elif config['target_model'] == 'ibm':
                sentence_result = verify_ibm_sentence(original_sentence, solution)
            elif config['target_model'] == 'microsoft':
                sentence_result = verify_microsoft_sentence(original_sentence, solution)

            if sentence_result['check']:
                index_list.append(index)
                sentence_result_list.append(sentence_result)

    for sentence_result in sentence_result_list:
        result_report = attack_model(config, sentence_result, result_report)

    success_num = result_report['[positive] success_num'] + result_report['[negative] success_num']
    if success_num != 0:
        result_report['avg_perturbed_ratio'] = round(result_report['avg_perturbed_ratio'] / success_num, 2)

    # results/amazon/[IMDB]positive_negative_result_1_1.csv
    filename = 'results/{0}/[{1}]{2}_{3}_result_{4}.csv'.format(
        config['target_model'], config['dataset'], config['source'], config['target_result'], config['length'])
    wirte_result(filename, result_report)
