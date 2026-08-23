import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('datasets/UNSW_NB15_cleaned.csv')

print('Full Dataset Label Distribution:')
print('=' * 60)
print(df['label'].value_counts())
print(f'\nPercentage: ')
print(df['label'].value_counts(normalize=True) * 100)

print('\n\nFirst 5000 samples Label Distribution:')
print('=' * 60)
print(df['label'].head(5000).value_counts())
print(f'\nPercentage: ')
print(df['label'].head(5000).value_counts(normalize=True) * 100)

print('\n\nLabel 0 count in first 5000:', (df['label'].head(5000) == 0).sum())
print('Label 1 count in first 5000:', (df['label'].head(5000) == 1).sum())
