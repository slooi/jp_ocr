from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
	QApplication,
	QLabel,
	QLineEdit,
	QMainWindow,
	QVBoxLayout,
	QWidget,
)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()	# You must always call this!
		self.setWindowTitle("hi") 
		self.checked = False
		
		# self.button = QPushButton("Push me!")
		# self.button.setChecked(False)
		# self.button.setCheckable(True)
		# self.button.clicked.connect(self.button_was_clicked)
		# self.setCentralWidget(self.button)



		# self.setFixedSize(QSize(400, 300))
		# self.setMinimumSize(QSize(1920,1080))
		# self.showMaximized()
		# self.showFullScreen()


		

		self.input = QLineEdit()

		self.label = QLabel()
		self.input.textChanged.connect(self.label.setText)

		layout = QVBoxLayout()
		layout.addWidget(self.input)
		layout.addWidget(self.label)

		container = QWidget()
		container.setLayout(layout)

		self.setCentralWidget(container)
		# self.setMouseTracking(True) 
		# self.label.setMouseTracking(True) 
		# self.input.setMouseTracking(True) 
		# container.setMouseTracking(True) 

	def button_was_clicked(self):
		self.checked = self.button.isChecked()
		self.button.setEnabled(False)
		print("hi",self.checked)

	def mouseMoveEvent(self, e):
		self.label.setText("mouseMoveEvent {} {}".format(e.globalX(),e.globalY()))
	def mousePressEvent(self, e):
		if e.button() == Qt.MouseButton.LeftButton:
			self.label.setText("mousePressEvent {} {}".format(e.globalX(),e.globalY()))
	def mouseReleaseEvent(self, e):
		if e.button() == Qt.MouseButton.LeftButton:
			self.label.setText("mouseReleaseEvent {} {}".format(e.globalX(),e.globalY()))
	

app = QApplication([])

window = MainWindow()
window.show()


app.exec()
