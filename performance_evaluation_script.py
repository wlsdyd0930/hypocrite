import subprocess

datasets = ['IMDB']
target_models = ['amazon', 'google', 'ibm', 'microsoft']
sources = ['positive', 'negative']
target_results = ['None', 'positive', 'negative', 'neutral', 'mixed']
lengths = ['1', '2', '3', '4', '5', '6', '7']
nums = ['1']


for dataset in datasets:
    command = 'python main.py'
    command_1 = command + ' --dataset ' + dataset
    for target_model in target_models:
        command_2 = command_1 + ' --target_model ' + target_model
        for source in sources:
            command_3 = command_2 + ' --source ' + source
            for target_result in target_results:
                if (target_model == 'google' or target_model == 'ibm') and target_result == 'mixed':
                    continue
                if source == target_result:
                    continue
                command_4 = command_3 + ' --target_result ' + target_result
                for length in lengths:
                    command_5 = command_4 + ' --length ' + length
                    for num in nums:
                        command_6 = command_5 + ' --num ' + num
                        print(command_6)
                        subprocess.run(command_6, shell=True)
