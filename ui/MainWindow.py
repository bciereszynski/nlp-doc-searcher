from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QWidget, QMainWindow, QVBoxLayout

from ui.DocumentWidget import DocumentWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search App')

        self.documentWidget = DocumentWidget()
        lay = QVBoxLayout()
        lay.addWidget(self.documentWidget, alignment=Qt.AlignHCenter | Qt.AlignTop )

        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)


    @staticmethod
    def __showErrorMsg(msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(msg)
        msgBox.setWindowTitle("Error")
        msgBox.exec_()
        return
