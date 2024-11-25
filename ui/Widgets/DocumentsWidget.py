from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QSizePolicy, QFileDialog

from backend.DocumentsProvider import DocumentsProvider
from ui.Widgets.SearchBar import SearchBar

class DocumentsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.documentsProvider = DocumentsProvider()

        self.searchBar = SearchBar()
        self.addButton = QPushButton('Add Document')
        self.documentsList = QListWidget()
        self.documentsList.setMinimumSize(200, 600)

        self.addButton.clicked.connect(self.add_document)
        self.searchBar.connectButtonClickedSlot(
            lambda: self.fetch_documents(self.searchBar.getQuery()))

        self.fetch_documents("")

        lay = QVBoxLayout()

        lay.addWidget(self.addButton, alignment=Qt.AlignCenter, stretch=1)
        lay.addWidget(self.searchBar, stretch=1)
        lay.addWidget(self.documentsList, stretch=10)

        self.setLayout(lay)

    def fetch_documents(self, query):
        documents = self.documentsProvider.get_ordered_documents(query)
        self.documentsList.clear()
        self.documentsList.addItems(documents)

    def add_document(self):
        fileName = QFileDialog.getOpenFileName(self)
        if not fileName[0]:
            return

        document = None
        with open(fileName[0], 'r') as f:
            document = f.read()

        if document is not None:
            self.documentsProvider.add_document(document)

        self.fetch_documents("")
