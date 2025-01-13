import logging

from PyQt5.QtWidgets import QApplication
import sys

from ui.MainWindow import MainWindow

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
