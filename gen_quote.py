import random
from pythainlp.tokenize import word_tokenize

# Word Tokenize
docs = []

with open('quote.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        docs.append(word_tokenize(line.strip()))

# Preprocessing
for i in range(len(docs)):
    new_doc = []

    for j in range(len(docs[i])):
        word = docs[i][j].lower().strip()

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

for n in graph:
    print(f'{n} -> {graph[n]}')

quotes = []
n = 13
for j in range(1, 101):
    output = []
    prev = '<START>'
    for i in range(n):
        word = random.choice(graph[prev])
        if word == '<END>':
            break
        output.append(word)
        prev = word
    # print(f'{j}) {"".join(output)}')
    quotes.append("".join(output))

quotes.sort(key=lambda q: len(q), reverse=True)
for i in range(1, 31):
    print(f'{i}. {quotes[i]}')