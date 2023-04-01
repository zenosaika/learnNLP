import numpy as np
import pandas as pd

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
        if 'www' in w:
            if doc:
                docs.append(doc)
                doc = []
            else:
                continue
        else:
            doc.append(w)
    docs.append(doc)
