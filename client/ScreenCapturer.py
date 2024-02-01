import time
from typing import Callable, List
from PySide6.QtCore import Qt, QRectF, Signal, QObject, QThread, QByteArray, QIODevice, QBuffer
from PySide6.QtGui import QPixmap, QPen
from PySide6.QtWidgets import (
	QApplication,
	QGraphicsSceneMouseEvent,
	QLabel,
	QMainWindow,
	QGraphicsItem,
)
from PySide6.QtWidgets import (
	QApplication,
	QGraphicsScene,
	QGraphicsView,
	QGraphicsRectItem,
	QGraphicsPixmapItem,
	QVBoxLayout,
	QWidget,
	QGraphicsColorizeEffect,
)
from PySide6.QtGui import QPixmap, QColor
import keyboard


class GraphicsScene(QGraphicsScene):
	def __init__(
		self,
		mousePressEventCallback=None,
		mouseMoveEventCallback=None,
		mouseReleaseEventCallback=None,
	):
		super().__init__()
		self.mousePressEventCallback = mousePressEventCallback
		self.mouseMoveEventCallback = mouseMoveEventCallback
		self.mouseReleaseEventCallback = mouseReleaseEventCallback

		# Set Size
		self.setSceneRect(0, 0, 1920, 1080)

	def add_item(self, item: QGraphicsPixmapItem):
		self.addItem(item)

	# SUBSCRIPTION
	def add_mouse_callbacks(
		self,
		mousePressEventCallback: Callable[[QGraphicsSceneMouseEvent], None],
		mouseMoveEventCallback: Callable[[QGraphicsSceneMouseEvent], None],
		mouseReleaseEventCallback: Callable[[QGraphicsSceneMouseEvent], None],
	):
		self.mousePressEventCallback = mousePressEventCallback
		self.mouseMoveEventCallback = mouseMoveEventCallback
		self.mouseReleaseEventCallback = mouseReleaseEventCallback

	# LISTENERS
	def mousePressEvent(self, event):
		if self.mousePressEventCallback:
			self.mousePressEventCallback(event)

	def mouseMoveEvent(self, event):
		if self.mouseMoveEventCallback:
			self.mouseMoveEventCallback(event)

	def mouseReleaseEvent(self, event):
		if self.mouseReleaseEventCallback:
			self.mouseReleaseEventCallback(event)
		# print(event.scenePos().x(),event.scenePos().y())


class GraphicsView(QGraphicsView):
	def __init__(self, graphics_scene: GraphicsScene):
		super().__init__(graphics_scene)

		# Set VIEW settings
		self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

		# Add red border
		self.setStyleSheet(
			"""
			border: 0px solid #000000;
			background-color: black;
		"""
		)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Set hints
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		# self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)


class MouseHandler:
	def __init__(self, graphics_scene: GraphicsScene) -> None:
		graphics_scene.add_mouse_callbacks(
			self.mouse_press_event, self.mouse_move_event, self.mouse_release_event
		)

		self.x_press = 0.0
		self.y_press = 0.0
		self.x_move = 0.0
		self.y_move = 0.0
		self.x_release = 0.0
		self.y_release = 0.0

	# SUBSCRIPTION
	def add_mouse_callbacks(
		self,
		mousePressEventCallback: Callable[[], None],
		mouseMoveEventCallback: Callable[[], None],
		mouseReleaseEventCallback: Callable[[], None],
	):
		self.mousePressEventCallback = mousePressEventCallback
		self.mouseMoveEventCallback = mouseMoveEventCallback
		self.mouseReleaseEventCallback = mouseReleaseEventCallback

	# LISTENERS
	def mouse_press_event(self, event: QGraphicsSceneMouseEvent):
		self.x_press = event.scenePos().x()
		self.y_press = event.scenePos().y()

		self.x_move = event.scenePos().x()  # Slight hack.......
		self.y_move = event.scenePos().y()  # Slight hack.......
		self.mousePressEventCallback()

	def mouse_move_event(self, event: QGraphicsSceneMouseEvent):
		self.x_move = event.scenePos().x()
		self.y_move = event.scenePos().y()
		self.mouseMoveEventCallback()

	def mouse_release_event(self, event: QGraphicsSceneMouseEvent):
		self.x_release = event.scenePos().x()
		self.y_release = event.scenePos().y()
		self.mouseReleaseEventCallback()

	# PRIVATE METHODS
	def mouse_positions_to_rect_shape(self):
		left, top, width, height = 0.0, 0.0, 0.0, 0.0

		x_press = self.x_press
		y_press = self.y_press
		x_move = self.x_move
		y_move = self.y_move

		# Horizontal Calculations
		if x_press < x_move:
			left = x_press
			width = x_move - x_press
		else:
			left = x_move
			width = x_press - x_move

		# Vertical Calculations
		if y_press < y_move:
			top = y_press
			height = y_move - y_press
		else:
			top = y_move
			height = y_press - y_move

		return [left, top, round(width), round(height)]


class ResizableRectItem(QGraphicsRectItem):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)
		self.setPen(QPen(QColor("red"), 1))
		self.setBrush(QColor(0, 0, 0, 0))

	def boundingRect(self):
		return QRectF(0, 0, 1920, 1080)


class ScreenCapturerSignaller(QObject):
	show = Signal()
	hide = Signal()
	delete = Signal()

	def __init__(self):
		super().__init__()
		print("Set triggers!")
		keyboard.add_hotkey("esc", self.hide.emit)
		keyboard.add_hotkey("left windows+`", self.show.emit)
		keyboard.add_hotkey("alt+z", self.show.emit)
		keyboard.add_hotkey("ctrl+c", self.delete.emit)
		# keyboard.wait()
	


class ScreenCapturer:
	def __init__(self) -> None:
		# App``
		self.app = QApplication([])

		# Create graphics SCENE
		self.graphics_scene = GraphicsScene()
		self.mouse_handler = MouseHandler(self.graphics_scene)
		self.mouse_handler.add_mouse_callbacks(
			self.mouse_press_event, self.mouse_move_event, self.mouse_release_event
		)
		# Create VIEW from SCENE
		self.graphics_view = GraphicsView(self.graphics_scene)

		# SETUP
		self.items: List[QGraphicsItem] = []

		# Create main window
		self.main_window = MainWindow()
		self.main_window.setWindowTitle("OCR")
		self.main_window.setCentralWidget(self.graphics_view)
		self.main_window.move(0,0)

		# Set the cursor to CrossCursor
		self.graphics_view.setCursor(Qt.CursorShape.CrossCursor)

		# self.main_window.showFullScreen()
		# self.main_window.show()
		self.main_window.setGeometry(0, 0, 1920, 1080)
		self.main_window.hide()

		#############################
		# ADD THREAD AND SIGNALLER
		self._thread = QThread(self.main_window)

		self.signaller_worker = ScreenCapturerSignaller()
		self.signaller_worker.moveToThread(self._thread)

		self.signaller_worker.hide.connect(self.hide)
		self.signaller_worker.show.connect(self.show)
		self.signaller_worker.delete.connect(self.delete)
		print("everything is connected")

	def add_screenshot(self):
		# Get screenshot
		screen = QApplication.primaryScreen()
		self.screenshot = screen.grabWindow(0)

		# Load & Display Image
		image_item = QGraphicsPixmapItem(self.screenshot)
		image_item.setOpacity(0.88)
		# image_item = QGraphicsPixmapItem(QPixmap("client/test2.png"))

		self.graphics_scene.addItem(image_item)
		self.items.append(image_item)

	def add_selection_area(self):
		if not self.screenshot:
			raise Exception("self.screenshot must be assigned first!")

		# 1) Crop screenshot
		self.cropped_pixmap = self.screenshot.copy(0, 0, 1, 1)
		# 1.1) Create a QGraphicsPixmapItem with the cropped image
		selection_screenshot = QGraphicsPixmapItem(self.cropped_pixmap)

		# 2) Create selection rect
		selection_rect = ResizableRectItem(0, 0, 1920-1, 1080-1)

		# Add the item to the scene``
		self.graphics_scene.addItem(selection_screenshot)
		self.graphics_scene.addItem(selection_rect)
		self.items.append(selection_screenshot)
		self.items.append(selection_rect)

	def mouse_press_event(self):
		pass

	def mouse_move_event(self):
		(left, top, width, height) = self.mouse_handler.mouse_positions_to_rect_shape()
		if width > 0 and height > 0:
			print(self.mouse_handler.mouse_positions_to_rect_shape())
			self.cropped_pixmap = self.screenshot.copy(
				*self.mouse_handler.mouse_positions_to_rect_shape()
			)
			selection_area = QGraphicsPixmapItem(self.cropped_pixmap)
			selection_area.setPos(left, top)

			selection_area2 = ResizableRectItem(
				*self.mouse_handler.mouse_positions_to_rect_shape()
			)
			# selection_area.setBoundingRegionGranularity()


			self.graphics_scene.removeItem(self.items[-1])
			self.graphics_scene.removeItem(self.items[-2])
			self.items.pop()
			self.items.pop()
			self.items.append(selection_area)
			self.items.append(selection_area2)
			self.graphics_scene.addItem(selection_area)
			self.graphics_scene.addItem(selection_area2)

	def mouse_release_event(self):
		convert_pixmap_to_bytes(self.cropped_pixmap)
		self.hide()

	def run(self):
		self.app.exec()

	def hide(self):
		self.main_window.hide()

	def delete(self):
		if self.graphics_view.hasFocus():
			print("QUITING")
			self.app.quit()

	def show(self):
		print("showing!")
		
		# Remove any items from previous region selection session
		for item in self.items:
			self.graphics_scene.removeItem(item)
		self.items = []

		# Add screenshot
		self.add_screenshot()
		
		# Add window border
		window_border = ResizableRectItem(0, 0, 1920-1, 1080-1)
		self.graphics_scene.addItem(window_border)
		self.items.append(window_border)

		# Add selection are
		self.add_selection_area()

		# DISPLAY
		self.main_window.showFullScreen()
		self.main_window.raise_()

		# self.main_window.showFullScreen()
		# self.main_window.show()
		# self.main_window.setFocus()
		# self.main_window.showMaximized()
		# self.main_window.activateWindow()
		# self.main_window.setWindowState(Qt.WindowState.WindowMaximized)
		# self.main_window.setWindowFlags(self.main_window.windowFlags() | Qt.Window)
		# self.main_window.activateWindow()
		# self.main_window.setWindowFlag(Qt.FramelessWindowHint, True)
		
def convert_pixmap_to_bytes(pixmap:QPixmap):
	buffer_array = QByteArray()

	buffer = QBuffer(buffer_array)
	buffer.open (QIODevice.OpenModeFlag.WriteOnly)

	ok = pixmap.save(buffer,"JPG")
	assert ok

	pixmap_bytes = buffer_array.data()
	# print("#pixmap_bytes")
	# print(pixmap_bytes)
	# print("^pixmap_bytes")
	return pixmap_bytes

if __name__ == "__main__":
	ocr_capture_app = ScreenCapturer()
	ocr_capture_app.run()
