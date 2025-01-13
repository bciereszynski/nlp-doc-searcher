from PyQt5.QtCore import QThread, pyqtSignal

class LoadDataWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, documents_provider, fetch_documents_callback):
        super().__init__()
        self.documents_provider = documents_provider
        self.fetch_documents_callback = fetch_documents_callback

    def run(self):
        self.documents_provider.init()
        self.fetch_documents_callback("")

        self.finished.emit()
