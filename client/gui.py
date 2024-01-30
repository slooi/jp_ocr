from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PySide6.QtCore import QSize, Qt

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()	# You must always call this!
		self.setWindowTitle("hi") 

		button = QPushButton("Push me!")
		self.setCentralWidget(button)

		# self.setFixedSize(QSize(400, 300))
		# self.setMinimumSize(QSize(1920,1080))
		# self.showMaximized()
		self.showFullScreen()
		
app = QApplication([])

window = MainWindow()
window.show()


app.exec()
