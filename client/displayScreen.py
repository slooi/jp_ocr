from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QColor


class GraphicsScene(QGraphicsScene):
	def __init__(self, parent=None):
		super().__init__(parent)

		# Set Size
		self.setSceneRect(0, 0, 1920, 1080)
		
		# Get screenshot
		screen = QApplication.primaryScreen()
		screenshot = screen.grabWindow(0)

		# Load & Display Image 
		image_item = QGraphicsPixmapItem(screenshot)
		# image_item = QGraphicsPixmapItem(QPixmap("client/test2.png"))
		self.addItem(image_item)

	def mousePressEvent(self, event):
		# Create a rectangle item at the mouse click position
		rect_item = QGraphicsRectItem(event.scenePos().x(), event.scenePos().y(), 50, 50)
		rect_item.setBrush(QColor("blue"))
		self.addItem(rect_item)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Set hints
		self.setWindowFlags(Qt.FramelessWindowHint)
		
		# Create graphics SCENE
		self.graphics_scene = GraphicsScene()

		# Create VIEW
		graphics_view = QGraphicsView(self.graphics_scene)

		# Set VIEW settings
		graphics_view.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		
		# Add red border
		graphics_view.setStyleSheet("""
			border: 1px solid #AA0000;
		""")
		
		# Add to window
		self.setCentralWidget(graphics_view)

		# Full screen window
		self.showFullScreen()



if __name__ == "__main__":
	# App
	app = QApplication([])

	# Create main window
	main_window = MainWindow()
	main_window.show()

	# Run
	app.exec()
	