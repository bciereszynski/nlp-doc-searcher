from enum import Enum

class SimilarityModel(Enum):
    TFIDF = 'TfIdfModel'
    GLOVE = 'Word2VecModel'
