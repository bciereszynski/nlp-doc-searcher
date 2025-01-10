import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QHBoxLayout, QLabel,
                             QMessageBox)
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

            list_widget.itemClicked.connect(self.show_document_preview)

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
            filenames = [doc['filename'] for doc in documents]

            self.documentsLists[model].clear()
            self.documentsLists[model].addItems(filenames)

    def add_document(self):
        fileName = QFileDialog.getOpenFileName(self)
        if not fileName[0]:
            return

        document = None
        with open(fileName[0], 'r') as f:
            document = f.read()

        if document is not None:
            base_name = os.path.basename(fileName[0])
            self.documentsProvider.add_document({'filename': base_name, 'content': document})

        self.fetch_documents(self.searchBar.getQuery())

    def show_document_preview(self, item):
        file_name = item.text()

        document_content = self.documentsProvider.get_document_content(file_name)

        if document_content is not None:
            msg = QMessageBox(self)
            msg.setWindowTitle(f"Preview: {file_name}")
            msg.setText(document_content)
            msg.exec_()
        else:
            QMessageBox.warning(self, "Error", f"Could not find content for file: {file_name}")
