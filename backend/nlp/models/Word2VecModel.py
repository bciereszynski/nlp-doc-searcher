import logging
from concurrent.futures import ThreadPoolExecutor

import nltk
import gensim.downloader as api
import numpy as np
from scipy import spatial

nltk.download('punkt_tab')


class Word2VecModel:
    __MODEL_NAME = "glove-wiki-gigaword-100"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.model = None
        self.vecs = {}

    def init(self, documents: list[str]) -> None:
        self.model = api.load(self.__MODEL_NAME)
        self.reinit(documents)
        self.logger.info("Word2VecModel initialized")

    def reinit(self, documents: list[str]) -> None:
        if documents:
            with ThreadPoolExecutor() as executor:
                results = executor.map(lambda doc: (doc, self.__calc_vector(doc)), documents)
            self.vecs = dict(results)

    def get_cosine_similarity(self, query: str):
        vec_query = self.__calc_vector(query)
        if vec_query is None:
            return np.zeros(len(self.vecs.items()))

        similarities = []
        for document, vec in self.vecs.items():
            similarities.append(spatial.distance.cosine(vec_query, vec))
        return similarities

    def __calc_vector(self, text: str):
        all_words = [word for word in nltk.word_tokenize(text)]
        vec_sum = np.zeros(self.model.vector_size)
        initialized = False

        for word in all_words:
            try:
                word_vec = self.model[word]
            except KeyError:
                continue
            initialized = True
            vec_sum = np.add(vec_sum, word_vec)

        if not initialized:
            return None
        return vec_sum
