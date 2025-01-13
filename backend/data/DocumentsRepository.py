import pickle

# Document is a dictionary with keys 'filename' and 'content'

class DocumentsRepository:
    __DEFAULT_DOCUMENTS_FILE = "documents.dat"

    def __init__(self, preprocessor, documents_file=__DEFAULT_DOCUMENTS_FILE):
        self.__preprocessor = preprocessor
        self.__documents = []
        self.__cleared_documents = []
        self.__documents_file = documents_file

    def init(self) -> None:
        self.load()

    def load(self) -> None:
        try:
            with open(self.__documents_file, "rb") as file:
                data = pickle.load(file)
                self.__documents = data.get("documents", [])
                self.__cleared_documents = data.get("cleared_documents", [])
        except FileNotFoundError:
            self.__documents = []
            self.__cleared_documents = []

    def save(self) -> None:
        data = {
            "documents": self.__documents,
            "cleared_documents": self.__cleared_documents,
        }
        with open(self.__documents_file, "wb") as outfile:
            pickle.dump(data, outfile)

    def add(self, document: dict) -> None:
        self.__documents.append(document)
        self.__cleared_documents.append(self.__preprocessor.preprocess(document['content']))

    def add_many(self, documents: list[dict]) -> None:
        cleared_documents = self.__preprocessor.preprocess_multiple([doc['content'] for doc in documents])
        self.__documents.extend(documents)
        self.__cleared_documents.extend(cleared_documents)

    def delete(self, filename_to_delete: str) -> None:
        self.__documents = [
            doc for doc in self.__documents if doc["filename"] != filename_to_delete
        ]
        self.__cleared_documents = [
            cleared_doc
            for doc, cleared_doc in zip(self.__documents, self.__cleared_documents)
            if doc["filename"] != filename_to_delete
        ]

    def delete_many(self, filenames_to_delete: list[str]) -> None:
        filenames_to_delete_set = set(filenames_to_delete)
        self.__documents = [
            doc for doc in self.__documents if doc["filename"] not in filenames_to_delete_set
        ]
        self.__cleared_documents = [
            cleared_doc
            for doc, cleared_doc in zip(self.__documents, self.__cleared_documents)
            if doc["filename"] not in filenames_to_delete_set
        ]

    def get_documents(self) -> list[dict]:
        return self.__documents

    def get_cleared_documents(self) -> list[str]:
        return self.__cleared_documents
