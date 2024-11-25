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
                self.cleared_documents = [self.preporcessor.preprocess(document) for document in self.documents]
        except FileNotFoundError:
            pass

    def save(self):
        with open("documents.dat", "w+b") as outfile:
            pickle.dump(self.documents, outfile)

    def add(self, document):
        self.documents.append(document)
        self.cleared_documents.append(self.preporcessor.preprocess(document))

    def delete(self, document):
        index = self.documents.index(document)
        self.documents.remove(index)
        self.cleared_documents.remove(index)

    def get_documents(self):
        return self.documents

    def get_clearded_documents(self):
        return self.cleared_documents
