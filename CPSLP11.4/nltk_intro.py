import nltk

from nltk.corpus import stopwords
sw_eng = stopwords.words('english')
stemmer = nltk.PorterStemmer()


def word_tokenize(filename):
    tokens = []
    for line in open(filename, 'r'):
        tokens.extend(nltk.word_tokenize(line.strip()))
    return tokens


def word_tokenize2(filename):
    tokens = []
    pattern = r'[a-zA-Z]+[-]?[a-zA-Z]*'
    for line in open(filename, 'r'):
        tokens.extend(nltk.tokenize.regexp_tokenize(line.strip(), pattern))
    return tokens


def token_frequencies(tokens):
    dict = {}
    for token in tokens:
        if token in dict:
            dict[token] +=1
        else:
            dict[token] = 1
    return dict

def remove_stopwords(tokens):
    result = tokens
    for token in tokens:
        if token in sw_eng:
            result.remove(token)
    return result

def stem_tokens(tokens):
    result = []
    for token in tokens:
        result.append(stemmer.stem(token))
    return result


tokens = word_tokenize2("scotland.txt")
print(tokens)
dict = token_frequencies(tokens)
print(dict)
print(len(dict))

tokens_without_stopwords = remove_stopwords(tokens)
print(tokens_without_stopwords)
dict2 = token_frequencies(tokens_without_stopwords)
print(dict2)
print(len(dict2))

stem_tokens_list = stem_tokens(tokens)
print(stem_tokens_list)
dict3 = token_frequencies(stem_tokens_list)
print(dict3)
print(len(dict3))


