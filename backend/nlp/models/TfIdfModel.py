import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.nlp.models.SimilarityModel import SimilarityModel


class TfIdfModel(SimilarityModel):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.vectorizer = TfidfVectorizer()
        self.documents_tfidf = None

    async def init_async(self, documents: list[str]) -> None:
        await self.reinit_async(documents)
        self.logger.info("TfIdfModel initialized")

    async def reinit_async(self, documents: list[str]) -> None:
        if documents:
            self.documents_tfidf = self.vectorizer.fit_transform(documents)

    def get_cosine_similarity(self, query: str):
        if self.documents_tfidf is None:
            return []
        query_tfidf = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_tfidf, self.documents_tfidf).flatten()
        return similarities
