import logging
import threading
from importlib import import_module

from backend.SimilarityModel import SimilarityModel
from backend.data.DocumentsRepository import DocumentsRepository
from backend.nlp.TextPreprocessor import TextPreprocessor


class DocumentsProvider:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.preprocessor = TextPreprocessor()
        self.repository = DocumentsRepository(self.preprocessor)

        self.models = {}
        for model in SimilarityModel:
            model_class_name = model.value
            module_path = f"backend.nlp.models.{model_class_name}"
            model_class = getattr(import_module(module_path), model_class_name)
            self.models[model] = model_class()

    def init(self):
        tasks = [
            self.preprocessor.init, self.repository.load
        ]
        threads = [self.__start_task(target, []) for target in tasks]
        for thread in threads:
            thread.join()
        logging.info("DocumentsProvider preprocessor and data initialized")

        cleared_documents = self.repository.get_cleared_documents()
        reinit_tasks = [
            (model.init, [cleared_documents]) for model in self.models.values()
        ]
        threads = [self.__start_task(target, args) for target, args in reinit_tasks]
        for thread in threads:
            thread.join()
        logging.info("DocumentsProvider models initialized")

    def add_document(self, document):
        self.repository.add(document)
        self.__reinit_models()

    def add_documents(self, documents):
        self.repository.add_many(documents)
        self.__reinit_models()

    def get_ordered_documents(self, query, model):
        documents = self.repository.get_documents()
        if query == "" or not documents:
            return documents

        if model not in self.models:
            raise ValueError(f"Unsupported model: {model}")

        similarities = self.models[model].get_cosine_similarity(self.preprocessor.preprocess(query))
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

    def __reinit_models(self):
        cleared_documents = self.repository.get_cleared_documents()
        reinit_tasks = [
            (model.reinit, [cleared_documents]) for model in self.models.values()
        ]
        threads = [self.__start_task(target, args) for target, args in reinit_tasks]
        for thread in threads:
            thread.join()

    def __start_task(self, target, args):
        thread = threading.Thread(target=target, args=args)
        thread.start()
        return thread
