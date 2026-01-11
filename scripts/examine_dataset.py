#!/usr/bin/env python3
from datasets import load_from_disk

dataset = load_from_disk('datasets/romansh')
print('Dataset structure:')
print(dataset)
print('\nSample examples:')

for i in range(min(5, len(dataset['train']))):
    print(f'\n--- Example {i+1} ---')
    prompt = dataset['train'][i]['Prompt']
    answer = dataset['train'][i]['Answer']
    print(f"Prompt: {prompt[:200]}")
    print(f"Answer: {answer[:200]}")
