import os
import pandas as pd

def get_dataset(dataset, length, source):
    if dataset == 'IMDB':
        file = "dataset/IMDB_Dataset.csv"
        if os.path.isfile(file):
            df = pd.read_csv(file)
            if length == 1:
                df = df.loc[df['review'].str.len() < 500]
            elif length == 2:
                df = df.loc[(df['review'].str.len() >= 500) & (df['review'].str.len() < 800)]
            elif length == 3:
                df = df.loc[(df['review'].str.len() >= 800) & (df['review'].str.len() < 1100)]
            elif length == 4:
                df = df.loc[(df['review'].str.len() >= 1100) & (df['review'].str.len() < 1400)]
            elif length == 5:
                df = df.loc[(df['review'].str.len() >= 1400) & (df['review'].str.len() < 1700)]
            elif length == 6:
                df = df.loc[(df['review'].str.len() >= 1700) & (df['review'].str.len() < 2000)]
            elif length == 7:
                df = df.loc[(df['review'].str.len() >= 2000) & (df['review'].str.len() < 2500)]

            if (source == 'positive') or (source == 'negative'):
                df = df.loc[df['sentiment'] == source]
        else:
            print("We can not find dataset file.")
    return df