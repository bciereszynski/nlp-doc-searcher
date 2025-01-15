import os
from concurrent.futures import ThreadPoolExecutor

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QHBoxLayout, QLabel,
                             QMessageBox)

from backend.DocumentsProvider import DocumentsProvider
from backend.SimilarityModel import SimilarityModel
from ui.Widgets.LoadingScreen import LoadingScreen
from ui.Widgets.SearchBar import SearchBar
from ui.utils.LoadDataWorker import LoadDataWorker


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

        vLay = QHBoxLayout()
        vLay.addWidget(self.addButton)
        vLay.addWidget(self.saveButton)

        lay = QVBoxLayout()

        lay.addLayout(vLay, stretch=1)
        lay.addWidget(self.searchBar, stretch=1)
        lay.addLayout(listsLayout, stretch=10)

        self.setLayout(lay)

        self.loading_screen = LoadingScreen()
        self.worker = None

    def load_data_and_show_loading(self):
        self.loading_screen.start_animation()
        self.parent().setEnabled(False)
        QTimer.singleShot(10, self.__load_data_and_models)

    def show_document_preview(self, item):
        file_name = item.text().split()[0]

        document_content = self.documentsProvider.get_document_content(file_name)

        if document_content is not None:
            msg = QMessageBox(self)
            msg.setWindowTitle(f"Preview: {file_name}")
            msg.setText(document_content)
            msg.exec_()
        else:
            QMessageBox.warning(self, "Error", f"Could not find content for file: {file_name}")

    def fetch_documents(self, query):
        for model in SimilarityModel:
            documents, similarities = self.documentsProvider.get_ordered_documents(query, model=model)
            filenames = [f"{documents[i]['filename']}\t{similarities[i]:.2%}" for i in range(len(documents))]

            self.documentsLists[model].clear()
            self.documentsLists[model].addItems(filenames)

    def add_document(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Documents", "", "Text Files (*.txt);;All Files (*)")

        if not file_names:
            return

        def read_document(file_name):
            with open(file_name, 'r') as f:
                return f.read()

        with ThreadPoolExecutor() as executor:
            documents = list(executor.map(read_document, file_names))

        documents = [doc for doc in documents if doc]
        dicts = [{'filename': os.path.basename(file_name), 'content': doc} for file_name, doc in
                 zip(file_names, documents)]

        self.documentsProvider.add_documents(dicts)

        self.fetch_documents(self.searchBar.getQuery())

    def __on_loading_finished(self):
        self.loading_screen.stop_animation()
        self.parent().setEnabled(True)

    def __load_data_and_models(self):
        self.worker = LoadDataWorker(self.documentsProvider, self.fetch_documents)
        self.worker.finished.connect(self.__on_loading_finished)
        self.worker.start()
