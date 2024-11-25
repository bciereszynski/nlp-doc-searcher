from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui.Widgets.SearchBar import SearchBar

class DocumentsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.searchBar = SearchBar()
        self.addButton = QPushButton('Add Document')

        lay = QVBoxLayout()
        lay.setSpacing(0)
        lay.addStretch(1)
        lay.addWidget(self.addButton, alignment=Qt.AlignCenter)
        lay.addWidget(self.searchBar)

        self.setLayout(lay)