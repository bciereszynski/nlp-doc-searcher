from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton

class SearchBar(QWidget):
    def __init__(self):
        super().__init__()

        self.lineEdit = QLineEdit()
        self.lineEdit.setMinimumWidth(600)
        self.button = QPushButton('Search')

        grid = QGridLayout()

        grid.addWidget(self.lineEdit, 0, 0, QtCore.Qt.AlignCenter)
        grid.addWidget(self.button, 1, 0, QtCore.Qt.AlignRight)

        self.setLayout(grid)
