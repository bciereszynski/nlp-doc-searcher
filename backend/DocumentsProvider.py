from backend.data.DocumentsRepository import DocumentsRepository
from backend.nlp.TextPreprocessor import TextPreprocessor
from backend.nlp.TfIdfModel import TfIdfModel


class DocumentsProvider:
    def __init__(self):
        self.preprocesor = TextPreprocessor()
        self.repository = DocumentsRepository(self.preprocesor)
        self.repository.load()
        self.Tfidf = TfIdfModel(self.repository.get_clearded_documents())

    def add_document(self, document):
        self.repository.add(document)
        self.Tfidf.reinit(self.repository.get_clearded_documents())

    def get_ordered_documents(self, query):
        documents = self.repository.get_documents()
        if query == "" or not documents:
            return documents

        similarities = self.Tfidf.get_cosine_similarity(self.preprocesor.preprocess(query))

        sorted_similarities = sorted(zip(similarities, documents), reverse=True)
        sorted_values, sorted_documents = zip(*sorted_similarities)

        return sorted_documents

    def save_data(self):
        self.repository.save()
