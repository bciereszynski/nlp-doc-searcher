from importlib import import_module

from backend.SimilarityModel import SimilarityModel
from backend.data.DocumentsRepository import DocumentsRepository
from backend.nlp.TextPreprocessor import TextPreprocessor

class DocumentsProvider:
    def __init__(self):
        self.preprocesor = TextPreprocessor()
        self.repository = DocumentsRepository(self.preprocesor)
        self.repository.load()

        self.models = {}
        for model in SimilarityModel:
            model_class_name = model.value
            module_path = f"backend.nlp.{model_class_name}"
            model_class = getattr(import_module(module_path), model_class_name)
            self.models[model] = model_class(self.repository.get_clearded_documents())

    def add_document(self, document):
        self.repository.add(document)
        cleared_documents = self.repository.get_clearded_documents()

        for model in self.models.values():
            model.reinit(cleared_documents)

    def get_ordered_documents(self, query, model):
        documents = self.repository.get_documents()
        if query == "" or not documents:
            return documents

        if model not in self.models:
            raise ValueError(f"Unsupported model: {model}")

        similarities = self.models[model].get_cosine_similarity(self.preprocesor.preprocess(query))
        sorted_similarities = sorted(zip(similarities, documents), key=lambda x: x[0], reverse=True)
        _, sorted_documents = zip(*sorted_similarities)

        return sorted_documents

    def save_data(self):
        self.repository.save()

    def get_document_content(self, filename):
        for document in self.repository.get_documents():
            if document['filename'] == filename:
                return document['content']
        raise ValueError(f"Document with filename '{filename}' not found.")
