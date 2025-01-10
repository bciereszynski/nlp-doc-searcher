import pickle

class DocumentsRepository:
    def __init__(self, preprocesor):
        self.preporcessor = preprocesor
        self.documents = []
        self.cleared_documents = []

    def load(self):
        try:
            with open("documents.dat", "rb") as file:
                self.documents = pickle.load(file)
                self.cleared_documents = [self.preprocessor.preprocess(document['content']) for document in
                                          self.documents]
        except FileNotFoundError:
            pass

    def save(self):
        with open("documents.dat", "wb") as outfile:
            pickle.dump(self.documents, outfile)

    def add(self, document):
        self.documents.append(document)
        self.cleared_documents.append(self.preprocessor.preprocess(document['content']))

    def delete(self, document):
        self.documents.remove(document)
        self.cleared_documents.remove(self.preprocessor.preprocess(document['content']))

    def get_documents(self):
        return self.documents

    def get_clearded_documents(self):
        return self.cleared_documents
