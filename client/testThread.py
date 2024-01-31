import time
from PySide6.QtCore import Qt, QRectF, QThread, Signal, QObject
from PySide6.QtGui import QPixmap, QPen
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsSceneMouseEvent,
    QLabel,
    QMainWindow,
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsPixmapItem,
    QVBoxLayout,
    QWidget,
)
import keyboard
import sys


class Worker(QObject):
    show = Signal()
    hide = Signal()

    def run(self):
        print("FINISHED EMIT!")
        keyboard.add_hotkey("ctrl+g", self.hide.emit)
        keyboard.add_hotkey("ctrl+h", self.show.emit)


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._thread = QThread(self)

        self.worker = Worker()
        self.worker.moveToThread(self._thread)

        self._thread.started.connect(self.worker.run)
        self.worker.show.connect(self.show_handler)
        self.worker.hide.connect(self.hide_handler)

        self._thread.start()

    def show_handler(self):
        self.showFullScreen()
        print("finished handler called!")

    def hide_handler(self):
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CustomMainWindow()
    main_window.show()
    app.exec()
