from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfIdfVectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.documents_tfidf = None

    def fit_transform_documents(self, documents):
        self.documents_tfidf = self.vectorizer.fit_transform(documents)
        return self.documents_tfidf

    def get_tfidf_query_similarity(self, query):
        query_tfidf = self.vectorizer.transform([query])

        similarities = cosine_similarity(query_tfidf, self.documents_tfidf).flatten()
        return similarities
