import nltk
import gensim.downloader as api
import numpy as np
from scipy import spatial

class Word2VecModel:
    # documents must be preprocessed
    def __init__(self, documents):
        self.model = api.load("glove-wiki-gigaword-50")
        self.vecs = {}
        for document in documents:
            self.vecs[document] = self.__calc_vector(document)

    def reinit(self, documents):
        self.vecs = {}
        for document in documents:
            self.vecs[document] = self.__calc_vector(document)

    # query must be preprocessed
    def get_cosine_similarity(self, query):
        vec_query = self.__calc_vector(query)
        if vec_query is None:
            return np.zeros(len(self.vecs.items()))
        similarities = []
        for document, vec in self.vecs.items():
            similarities.append(spatial.distance.cosine(vec_query, vec))
        return similarities

    def __calc_vector(self, text):
        all_words = [word for word in nltk.word_tokenize(text)]
        vec_sum = np.zeros(self.model.vector_size)
        initialized = False

        for word in all_words:
            try:
                word_vec = self.model[word]
            except KeyError as e:
                continue
            initialized = True
            vec_sum  = np.add(vec_sum, word_vec)

        if not initialized:
            return None
        return vec_sum
