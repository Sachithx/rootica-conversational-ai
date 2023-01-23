print(" ")
print("Starting the Search Engine!!")
import json
import pandas as pd
import html
from bs4 import BeautifulSoup
import re
import string
import pandas as pd
import nltk
import nltk.corpus.reader.wordnet as wn
from nltk.stem import WordNetLemmatizer
from rank_bm25 import BM25Okapi
import numpy as np

# Opening JSON file
f = open('product_data.json')

# returns JSON object as a dictionary
data = json.load(f)

# Closing file
f.close()

products = []

for prod in data:
        dict = {
                "product_id": None,
                "product_name": None,
                "price": None,
                "available": None,
                "skin_type": None,
                "ingredients": None,
                "image": None,
                "checkout_url": None
        }

        ## Product ID
        dict["product_id"] = prod.get('id')      
        
        ## Product Name
        dict["product_name"] = prod.get('name')            
        
        ## Price
        dict["price"] = prod.get('price') 

        ## Availability
        dict["available"] = True if prod.get('stock_status')=='instock' else False 

        ## Dosha Types
        for i in prod.get('attributes'):
                if i.get('name')=="Dosha Types":
                        dict["skin_type"] = html.unescape(i.get('options')[0])

        ## Ingredients
        for i in prod.get('attributes'):
                if i.get('name')=="Wonder Herbs":
                        dict["ingredients"] = i.get('options')  
        
        ## Images
        for i in prod.get('images'):
                dict["image"] = prod.get('images')[0].get('src')

        ## Purchase Link
        dict["checkout_url"] = prod.get('permalink')

        products.append(dict)


stopword_list = nltk.corpus.stopwords.words('english')
wnl = WordNetLemmatizer()

def tokenize_text(text):
    tokens = nltk.word_tokenize(text) 
    tokens = [token.strip() for token in tokens]
    return tokens

# Annotate text tokens with POS tags
def pos_tag_text(text):
    
    def penn_to_wn_tags(pos_tag):
        if pos_tag.startswith('J'):
            return wn.ADJ
        elif pos_tag.startswith('V'):
            return wn.VERB
        elif pos_tag.startswith('N'):
            return wn.NOUN
        elif pos_tag.startswith('R'):
            return wn.ADV
        else:
            return None

    tokens = nltk.word_tokenize(text)
    tagged_text = nltk.pos_tag(tokens)
    tagged_lower_text = [(word.lower(), penn_to_wn_tags(pos_tag))
                         for word, pos_tag in
                         tagged_text]
    return tagged_lower_text

# lemmatize text based on POS tags    
def lemmatize_text(text):
    pos_tagged_text = pos_tag_text(text)
    lemmatized_tokens = [wnl.lemmatize(word, pos_tag) if pos_tag
                         else word                     
                         for word, pos_tag in pos_tagged_text]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text

def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub(' ', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text

# We generalize and parameterize our normalize operation
def normalize_corpus(corpus, lemmatize=True, stopwords=True):
    normalized_corpus = []  
    for text in corpus:
        ## Lowercase letters
        text = text.lower()
        ## Contraction map
        #text = expand_contractions(text, CONTRACTION_MAP)
        if lemmatize:
        ## Lemmatization
            text = lemmatize_text(text)
        else:
            text = text.lower()
        ## Remove special Characters
        text = remove_special_characters(text)
        if stopwords:
        ## Remove stopwords
            text = remove_stopwords(text)
            normalized_corpus.append(text)
        else:
            normalized_corpus.append(text)
            
    return normalized_corpus

# We generalize and parameterize our normalize operation
def normalize_string(string, lemmatize=True, stopwords=True):
    normalized_string = []  
    string = [string]
    for text in string:
        ## Lowercase letters
        text = text.lower()
        ## Contraction map
        #text = expand_contractions(text, CONTRACTION_MAP)
        if lemmatize:
        ## Lemmatization
            text = lemmatize_text(text)
        else:
            text = text.lower()
        ## Remove special Characters
        text = remove_special_characters(text)
        if stopwords:
        ## Remove stopwords
            text = remove_stopwords(text)
            normalized_string.append(text)
        else:
            normalized_string.append(text)
            
    return normalized_string

data = []
for i in products:
    name = i.get('product_name')
    data.append(name)

# Normalize the corpus as usual
norm_product_names = normalize_corpus(data, lemmatize=True, stopwords=True)

corpus = norm_product_names
tokenized_corpus = [name.split(" ") for name in corpus]
tokenized_corpus = []
for name in corpus:
    #print(name)
    doc_tokens = name.split()
    #print(doc_tokens)
    tokenized_corpus.append(doc_tokens)

import re

def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

tok_list = []
for name in corpus:
    a = name.split() + ngrams(name, 1) + ngrams(name, 2) + ngrams(name, 3)
    tok_list.append(a)

bm25 = BM25Okapi(tok_list)


def search(name, num_bm=5):
    print(" ")
    input = name
    for n in normalize_string(input):
        new_name = n
    tokenized_name = new_name.split() + ngrams(new_name, 2) + ngrams(new_name, 3) + ngrams(new_name, 4)
    doc_scores = bm25.get_scores(tokenized_name)
    max = np.max(doc_scores)
    print(f"Highest BM25 Score: {max}")
    print(" ")
    if max < 20.0:
        print("The BM25 score is bellow the threshold.")
        print('No matching results')
    else:
        print("Here are the best matching results...")
        print(*bm25.get_top_n(tokenized_name, corpus, n=num_bm), sep='\n')
    print("Searching completed!!")
    print(" ")

name = input('Enter Product Name: ')
search(name)