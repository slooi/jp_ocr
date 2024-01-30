from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QColor


class DrawingScene(QGraphicsScene):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setSceneRect(0, 0, 1920, 1080)

	def mousePressEvent(self, event):

		# Load an image and add it to the scene at the same position as the rectangle
		# screen = QApplication.primaryScreen()
		# screenshot = screen.grabWindow(0)
		image_item = QGraphicsPixmapItem(QPixmap("client/test2.png"))
		# image_item.setOffset(300, 300)
		image_item.setPos(0,0)
		# image_item.setPos(event.scenePos())
		self.addItem(image_item)
		# Create a rectangle item at the mouse click position
		rect_item = QGraphicsRectItem(event.scenePos().x(), event.scenePos().y(), 50, 50)
		rect_item.setBrush(QColor("blue"))
		self.addItem(rect_item)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Get screenshot
		screen = QApplication.primaryScreen()
		screenshot = screen.grabWindow(0)

		# Set the frameless window hint
		self.setWindowFlags(Qt.FramelessWindowHint)

		# Display screenshot
		self.label = QLabel()
		self.label.setPixmap(screenshot)
		# self.label.setPixmap(QPixmap("client/test.jpg"))

		self.drawing_scene = DrawingScene()

		layout = QVBoxLayout()
		# layout.addWidget(self.label)
		# layout.addWidget(self.drawing_scene)
		drawing_view = QGraphicsView(self.drawing_scene)
		
		drawing_view.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		layout.addWidget(drawing_view)

		container = QWidget()
		container.setLayout(layout)

		self.setCentralWidget(container)

		# 
		self.showFullScreen()
		
		

if __name__ == "__main__":

	# App
	app = QApplication([])

	main_window = MainWindow()
	main_window.show()

	# 
	app.exec()
	

""" 


class ScreenshotApp:
	def __init__(self):
		self.app = QApplication([])
		self.screen = QApplication.primaryScreen()
		self.screenshot = self.screen.grabWindow(0)
		
		self.window = QMainWindow()
		# self.window.setWindowFlags(Qt.FramelessWindowHint)  # Set the frameless window hint

		self.label = QLabel()
		self.label.setPixmap(self.screenshot)
		self.label.show()
		# self.label.setPixmap(QPixmap("test.jpg"))

	def run(self):
		self.app.exec()

if __name__ == "__main__":
	app_instance = ScreenshotApp()
	app_instance.run()
 """
