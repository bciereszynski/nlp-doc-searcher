from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox, QWidget, QMainWindow, QVBoxLayout

from ui.Widgets.DocumentsWidget import DocumentsWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search App')
        self.setMaximumWidth(500)
        self.setMaximumHeight(700)

        self.documentWidget = DocumentsWidget()
        lay = QVBoxLayout()
        lay.addWidget(self.documentWidget, alignment=Qt.AlignHCenter | Qt.AlignTop )

        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)

    def showEvent(self, event):
        self.documentWidget.load_data_and_show_loading()
        super().showEvent(event)

    @staticmethod
    def __showErrorMsg(msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(msg)
        msgBox.setWindowTitle("Error")
        msgBox.exec_()
        return
