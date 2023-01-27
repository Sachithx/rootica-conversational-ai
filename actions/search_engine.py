import re
import string
import nltk
import nltk.corpus.reader.wordnet as wn
from nltk.stem import WordNetLemmatizer
from rank_bm25 import BM25Okapi
import numpy as np
from FA2.boto3_dynamodb import DynamoDBCRUD

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
    wnl = WordNetLemmatizer()
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
    stopword_list = nltk.corpus.stopwords.words('english')
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

def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]


class SearchEngine():
    def __init__(self):  
        boto3_dynamodb = DynamoDBCRUD()
        self.products_db = boto3_dynamodb.get_all().values()

    def preprocess(self):
        names = []
        ids = []
        for i in self.products_db:
            name = i.get('product_name')
            id = i.get('product_id')
            names.append(name)
            ids.append(id)

        # Normalize the corpus as usual
        norm_product_names = normalize_corpus(names, lemmatize=True, stopwords=True)

        corpus = norm_product_names
        tokenized_corpus = [name.split(" ") for name in corpus]
        tokenized_corpus = []
        for name in corpus:
            doc_tokens = name.split()
            tokenized_corpus.append(doc_tokens)

        tok_list = []
        for name in corpus:
            a = name.split() + ngrams(name, 1) + ngrams(name, 2) + ngrams(name, 3)
            tok_list.append(a)
        return tok_list, ids

    def bm_25(self, tok_list):
        bm25 = BM25Okapi(tok_list)
        return bm25

    def search(self, bm25, name, ids, num_bm=1):
        if name!=None:
            input = name
            for n in normalize_string(input):
                new_name = n
            tokenized_name = new_name.split() + ngrams(new_name, 2) + ngrams(new_name, 3) + ngrams(new_name, 4)
            doc_scores = bm25.get_scores(tokenized_name)
            max = np.max(doc_scores)
            if max < 20.0:
                result = None
            else:
                result = bm25.get_top_n(tokenized_name, ids, n=num_bm)
        else:
            result = None 
        return result
