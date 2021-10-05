import argparse
from attack import start_attack

parser = argparse.ArgumentParser(description='Adversarial Attack for Text')
parser.add_argument('--dataset', default='IMDB', help='(i) IMDB')
parser.add_argument('--target_model', default='microsoft', help='(i) amazon - Amazone Comprehend (ii) google - Google Cloud NLP (iii) ibm - IBM Waston Natural Language Understanding (iv) microsoft - Microsoft Azure Text Analytics')
parser.add_argument('--source', default='negative', help='(i) None (ii) positive (iii) negative')
parser.add_argument('--target_result', default='neutral', help='(i) None - Non-target (ii) positive (iii) negative (iv) mixed (v) neutral')
parser.add_argument('--length', default=1, type=int, help='Text Length Group (i) x < 500  (ii) 500 <= x < 800 (iii) 800 <= x < 1100 (iv) 1100 <= x < 1400 (v) 1400 <= x < 1700 (vi) 1700 <= x < 2000 (vii) 2000 <= x < 2500')
parser.add_argument('--num', default=1, type=int, help='Text Num')

args = parser.parse_args()
if args.target_model == 'None':
    args.target_model = None
if args.target_result == 'None':
    args.target_result = None

config = {
    'dataset': args.dataset,
    'target_model': args.target_model,
    'source': args.source,
    'target_result': args.target_result,
    'length': args.length,
    'sentence_num': args.num
}

start_attack(config)