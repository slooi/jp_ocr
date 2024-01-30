from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QGraphicsSceneMouseEvent, QLabel, QMainWindow
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QColor


class GraphicsScene(QGraphicsScene):
	def __init__(self,mousePressEventCallback,mouseMoveEventCallback):
		super().__init__()
		self.mousePressEventCallback = mousePressEventCallback
		self.mouseMoveEventCallback = mouseMoveEventCallback

		# Set Size
		self.setSceneRect(0, 0, 1920, 1080)

	def add_item(self,item:QGraphicsPixmapItem):
		self.addItem(item)
		
	def mousePressEvent(self, event):
		self.mousePressEventCallback(event)

	def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
		self.mouseMoveEventCallback(event)
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
		

class OCRCaptureApp():
	def __init__(self) -> None:
		# App
		self.app = QApplication([])


		# Create graphics SCENE
		self.graphics_scene = GraphicsScene(self.mouse_press_event,self.mouse_move_event)
		# Create VIEW from SCENE
		self.graphics_view = GraphicsView(self.graphics_scene)


		# SETUP
		self.setup()


		# Create main window
		self.main_window = MainWindow()
		self.main_window.setCentralWidget(self.graphics_view)
		# Full screen window
		self.main_window.showFullScreen()
	
	def setup(self):
		self.add_screenshot()
		self.add_rectangle_SETUP()

	def add_screenshot(self):
		# Get screenshot
		screen = QApplication.primaryScreen()
		screenshot = screen.grabWindow(0)

		# Load & Display Image 
		image_item = QGraphicsPixmapItem(screenshot)
		# image_item = QGraphicsPixmapItem(QPixmap("client/test2.png"))

		self.graphics_scene.addItem(image_item)

	def add_rectangle_SETUP(self):
		# Create selection area
		self.selection_area = QGraphicsRectItem(0, 0, 50, 50)
		self.selection_area.setBrush(QColor("blue"))

		self.graphics_scene.addItem(self.selection_area)

	def mouse_move_event(self,event):
		self.selection_area.setRect(0,0,event.scenePos().x(),event.scenePos().y())
	def mouse_press_event(self,event):
		self.selection_area.setRect(0,0,event.scenePos().x(),event.scenePos().y())
	def mouse_release_event(self):
		pass
	def run(self):
		self.app.exec()

if __name__ == "__main__":
	ocr_capture_app = OCRCaptureApp()
	ocr_capture_app.run()