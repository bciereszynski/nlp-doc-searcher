from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfIdfModel:
    # documents must be preprocessed
    def __init__(self, documents):
        self.vectorizer = TfidfVectorizer()
        self.documents_tfidf = self.vectorizer.fit_transform(documents)

    def reinit(self, documents):
        self.documents_tfidf = self.vectorizer.fit_transform(documents)

    # query must be preprocessed
    def get_cosine_similarity(self, query):
        query_tfidf = self.vectorizer.transform([query])

        similarities = cosine_similarity(query_tfidf, self.documents_tfidf).flatten()
        return similarities
