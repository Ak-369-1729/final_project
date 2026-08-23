import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('datasets/UNSW_NB15_cleaned.csv')

print('Dataset Info:')
print('=' * 60)
print(f'Total rows: {len(df)}')
print(f'Label column dtype: {df["label"].dtype}')
print(f'\nLabel value counts:')
print(df['label'].value_counts())
print(f'\nLabel value counts (normalized):')
print(df['label'].value_counts(normalize=True))
print(f'\nUnique label values: {df["label"].unique()}')
print(f'\nLabel distribution percentage:')
print(df['label'].value_counts(normalize=True) * 100)
