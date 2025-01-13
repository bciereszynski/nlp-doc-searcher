from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setFixedSize(400, 400)

        self.setStyleSheet("border: 4px solid black;")

        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, self.width(), self.height())
        self.frame.setStyleSheet(
            "border:4px solid black;"
        )

        layout = QVBoxLayout(self.frame)
        layout.setAlignment(Qt.AlignCenter)

        self.label_animation = QLabel(self.frame)
        self.label_animation.setStyleSheet("border:none;")
        self.label_animation.setAlignment(Qt.AlignCenter)

        self.movie = QMovie('ui/assets/loading.gif')
        self.label_animation.setMovie(self.movie)

        scaled_width = int(self.frame.width() * 0.75)
        scaled_height = int(self.frame.height() * 0.75)
        self.movie.setScaledSize(QtCore.QSize(scaled_width, scaled_height))

        layout.addWidget(self.label_animation)

        self.label_text = QLabel("Models are loading ...", self.frame)
        self.label_text.setStyleSheet("border:none;")
        self.label_text.setAlignment(Qt.AlignCenter)
        self.label_text.setWordWrap(True)
        self.label_text.setStyleSheet("border:none; color: white; font-size: 36px; margin-top: 10px;")
        layout.addWidget(self.label_text)

    def start_animation(self):
        self.show()
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
        self.close()
