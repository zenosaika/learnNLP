import numpy as np
import pandas as pd
import random

# [Import Corpus] - from https://aiforthai.in.th/corpus.php
news = []
for i in range(1, 97):
    with open(f'news/news_{i:05}.txt', 'r') as f:
        news.append(f.read())

# [Preprocessing] - output: docs -> [ 
#                                     ['ไก่', 'กา', ..., '\n'], 
#                                     ['<NE>อาราเร่</NE>', ' ', ..., 'หงะ'], 
#                                   ]
docs = []
for n in news:
    words = n.split('|')
    doc = []
    for w in words:
        if ('www' in w) or ('WWW' in w):
            if doc:
                docs.append(doc)
                doc = []
            else:
                continue
        else:
            doc.append(w)
    # docs.append(doc)

# [Preprocessing] - remove NER -> strip space -> text to lower
for i in range(len(docs)):
    new_doc = []

    for j in range(len(docs[i])):
        word = docs[i][j].lower().strip()

        # remove tags
        for tag in ('<ne>', '</ne>', '<ab>', '</ab>', '<poem>', '</poem>'):
            word = word.replace(tag, '')

        # remove digits
        for digit in '0123456789':
            word = word.replace(digit, '')

        # remove punctuations
        punctuations = '''!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~'''
        for punctuation in punctuations:
            word = word.replace(punctuation, '')

        if word != '':
            new_doc.append(word)

    docs[i] = new_doc

# Markov Model
graph = {}

for doc in docs[:100]:
    prev = '<START>'
    for word in doc+['<END>']:
        if prev not in graph:
            graph[prev] = [word]
        else:
            graph[prev].append(word)
        prev = word

# Driver Code
n = 15
for j in range(30):
    output = []
    prev = '<START>'
    for i in range(n):
        word = random.choice(graph[prev])
        if word == '<END>':
            break
        output.append(word)
        prev = word
    print(f'{j}) {"".join(output)}')
