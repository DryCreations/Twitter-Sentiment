import os

# NOTE: download the imdb dataset from 
# http://ai.stanford.edu/~amaas/data/sentiment/
# then unzip it into backend/
def get_imdb(typ: str) -> list:
    reviews = []
    for filename in os.listdir(f'./aclImdb/train/{typ}/'):
        with open(f'./aclImdb/train/{typ}/{filename}', 'r', encoding='utf-8') as f:
            reviews.append(f.read())
    for filename in os.listdir(f'./aclImdb/test/{typ}/'):
        with open(f'./aclImdb/test/{typ}/{filename}', 'r', encoding='utf-8') as f:
            reviews.append(f.read())
    return reviews
