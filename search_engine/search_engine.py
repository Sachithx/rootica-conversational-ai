import re
import string
import nltk
import nltk.corpus.reader.wordnet as wn
from nltk.stem import WordNetLemmatizer
from rank_bm25 import BM25Okapi
import numpy as np
from api_endpoints.boto3_dynamodb import DynamoDBCRUD


class PreProcessSE:
    def __init__(self) -> None:
        pass

    @staticmethod
    def tokenize_text(text):
        tokens = nltk.word_tokenize(text)
        tokens = [token.strip() for token in tokens]
        return tokens

    # Annotate text tokens with POS tags
    @staticmethod
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
        tagged_lower_text = [(word.lower(), penn_to_wn_tags(pos_tag)) for word, pos_tag in tagged_text]
        return tagged_lower_text

    # lemmatize text based on POS tags    
    def lemmatize_text(self, text):
        wnl = WordNetLemmatizer()
        pos_tagged_text = self.pos_tag_text(text)
        lemmatized_tokens = [wnl.lemmatize(word, pos_tag) if pos_tag else word for word, pos_tag in pos_tagged_text]
        lemmatized_text = ' '.join(lemmatized_tokens)
        return lemmatized_text

    def remove_special_characters(self, text):
        tokens = self.tokenize_text(text)
        pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
        filtered_tokens = filter(None, [pattern.sub(' ', token) for token in tokens])
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    def remove_stopwords(self, text):
        stopword_list = nltk.corpus.stopwords.words('english')
        tokens = self.tokenize_text(text)
        filtered_tokens = [token for token in tokens if token not in stopword_list]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    # We generalize and parameterize our normalize operation
    def normalize_corpus(self, corpus, lemmatize=True, stopwords=True):
        normalized_corpus = []
        for text in corpus:
            # Lowercase letters
            text = text.lower()
            # Contraction map
            if lemmatize:
                # Lemmatization
                text = self.lemmatize_text(text)
            else:
                text = text.lower()
            # Remove special Characters
            text = self.remove_special_characters(text)
            if stopwords:
                # Remove stopwords
                text = self.remove_stopwords(text)
                normalized_corpus.append(text)
            else:
                normalized_corpus.append(text)

        return normalized_corpus

    # We generalize and parameterize our normalize operation
    def normalize_string(self, string, lemmatize=True, stopwords=True):
        normalized_string = []
        string = [string]
        for text in string:
            # Lowercase letters
            text = text.lower()
            if lemmatize:
            # Lemmatization
                text = self.lemmatize_text(text)
            else:
                text = text.lower()
            # Remove special Characters
            text = self.remove_special_characters(text)
            if stopwords:
            # Remove stopwords
                text = self.remove_stopwords(text)
                normalized_string.append(text)
            else:
                normalized_string.append(text)
        return normalized_string

    @staticmethod
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
        norm_product_names = PreProcessSE().normalize_corpus(names, lemmatize=True, stopwords=True)

        corpus = norm_product_names
        tokenized_corpus = [name.split(" ") for name in corpus]
        tokenized_corpus = []
        for name in corpus:
            doc_tokens = name.split()
            tokenized_corpus.append(doc_tokens)

        tok_list = []
        for name in corpus:
            a = name.split() + PreProcessSE().ngrams(name, 1) + PreProcessSE().ngrams(name, 2) + PreProcessSE().ngrams(name, 3)
            tok_list.append(a)
        return tok_list, ids

    @staticmethod
    def bm_25(tok_list):
        bm25 = BM25Okapi(tok_list)
        return bm25

    @staticmethod
    def search(bm25, name, ids, num_bm=1):
        if name is not None:
            input = name
            new_name = ""
            for n in PreProcessSE().normalize_string(input):
                new_name = n
            tokenized_name = new_name.split() + PreProcessSE().ngrams(new_name, 2) \
                             + PreProcessSE().ngrams(new_name, 3) + PreProcessSE().ngrams(new_name, 4)
            doc_scores = bm25.get_scores(tokenized_name)
            max = np.max(doc_scores)
            if max < 20.0:
                result = None
            else:
                result = bm25.get_top_n(tokenized_name, ids, n=num_bm)
        else:
            result = None
        return result
