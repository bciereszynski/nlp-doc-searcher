from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QHBoxLayout, QLabel

from backend.DocumentsProvider import DocumentsProvider
from backend.SimilarityModel import SimilarityModel
from ui.Widgets.SearchBar import SearchBar

class DocumentsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.documentsProvider = DocumentsProvider()

        self.searchBar = SearchBar()
        self.addButton = QPushButton('Add Document')
        self.saveButton = QPushButton('Save Documents')
        self.documentsLists = {model: QListWidget(self) for model in SimilarityModel}

        listsLayout = QHBoxLayout()

        for model, list_widget in self.documentsLists.items():
            columnLayout = QVBoxLayout()

            label = QLabel(model.name)
            columnLayout.addWidget(label)

            list_widget.setMinimumSize(200, 600)
            columnLayout.addWidget(list_widget)

            listsLayout.addLayout(columnLayout)

        self.addButton.clicked.connect(self.add_document)
        self.saveButton.clicked.connect(self.documentsProvider.save_data)
        self.searchBar.connectSearchSlot(
            lambda: self.fetch_documents(self.searchBar.getQuery()))

        self.fetch_documents("")

        vLay = QHBoxLayout()
        vLay.addWidget(self.addButton)
        vLay.addWidget(self.saveButton)

        lay = QVBoxLayout()

        lay.addLayout(vLay, stretch=1)
        lay.addWidget(self.searchBar, stretch=1)
        lay.addLayout(listsLayout, stretch=10)

        self.setLayout(lay)

    def fetch_documents(self, query):
        for model in SimilarityModel:
            documents = self.documentsProvider.get_ordered_documents(query, model=model)
            self.documentsLists[model].clear()
            self.documentsLists[model].addItems(documents)

    def add_document(self):
        fileName = QFileDialog.getOpenFileName(self)
        if not fileName[0]:
            return

        document = None
        with open(fileName[0], 'r') as f:
            document = f.read()

        if document is not None:
            self.documentsProvider.add_document(document)

        self.fetch_documents(self.searchBar.getQuery())
