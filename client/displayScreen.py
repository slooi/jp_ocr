from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QLabel, QMainWindow
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


		# Create selection area
		self.selection_area = QGraphicsRectItem(0, 0, 50, 50)
		self.selection_area.setBrush(QColor("blue"))
		self.addItem(self.selection_area)

	def add_item(self,item:QGraphicsPixmapItem):
		self.addItem(item)
		
	def mousePressEvent(self, event):
		self.selection_area.setRect(0,0,event.scenePos().x(),event.scenePos().y())

	def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
		self.selection_area.setRect(0,0,event.scenePos().x(),event.scenePos().y())
		# print(event.scenePos().x(),event.scenePos().y())

class GraphicsView(QGraphicsView):
	def __init__(self,graphics_scene:GraphicsScene):
		super().__init__(graphics_scene)

		# Set VIEW settings
		self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		
		# Add red border
		self.setStyleSheet("""
			border: 1px solid #AA0000;
		""")
		


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Set hints
		self.setWindowFlags(Qt.FramelessWindowHint)
		
		# Create graphics SCENE
		self.graphics_scene = GraphicsScene()

		# Create VIEW
		graphics_view = GraphicsView(self.graphics_scene)
		
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
	