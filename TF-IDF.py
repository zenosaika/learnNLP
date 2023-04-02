import numpy as np
import pandas as pd
from pythainlp.corpus import thai_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

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

        stop_words = thai_stopwords()

        if (word != '') and (word not in stop_words):
            new_doc.append(word)

    docs[i] = new_doc

# [Calculate] - TF-IDF
tfidf_vectorizer = TfidfVectorizer(analyzer='word',
                                   tokenizer=lambda text: text,
                                   preprocessor=lambda text: text,
                                   token_pattern=None)

tfidf_vector = tfidf_vectorizer.fit_transform(docs[:100])
tfidf_array = np.array(tfidf_vector.todense())

tfidf_df = pd.DataFrame(tfidf_array, columns=tfidf_vectorizer.get_feature_names_out())
top_tfidf_df = tfidf_df.apply(lambda r: r.nlargest(10).index.tolist(), axis=1).ravel()
print(top_tfidf_df)
