import signal
import sys
import time
from typing import Any, Callable, List, Optional
from PySide6.QtCore import Qt, QRectF, Signal, QObject, QThread, QByteArray, QIODevice, QBuffer, QRunnable, QThreadPool, QCoreApplication
from PySide6.QtGui import QPixmap, QPen
from PySide6.QtWidgets import (
	QApplication,
	QGraphicsSceneMouseEvent,
	QLabel,
	QMainWindow,
	QGraphicsItem,
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
from pydantic import BaseModel
from HotkeyHandler import Hotkey
from PySide6.QtCore import QObject, Signal, Slot, SLOT

from main import KnownError, TwoPoints, post_image

from HotkeyHandler import Hotkey, WindowsHotkeyHandler
from abc import ABC, abstractmethod
import traceback

#########################################################################################
#########################################################################################
#########################################################################################

class HotkeyRunnable(QRunnable):
	def __init__(self,hotkeys:List[Hotkey]) -> None:
		super().__init__()
		self.hotkeys=hotkeys

	def run(self):
		WindowsHotkeyHandler(self.hotkeys)

#########################################################################################
#########################################################################################
#########################################################################################

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


#########################################################################################
#########################################################################################
#########################################################################################

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

#########################################################################################
#########################################################################################
#########################################################################################

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Set hints
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		# self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)


class MouseHandler:
	def __init__(self, graphics_scene: GraphicsScene,
		mousePressEventCallback: Callable[[], None],
		mouseMoveEventCallback: Callable[[], None],
		mouseReleaseEventCallback: Callable[[], None]) -> None:
		graphics_scene.add_mouse_callbacks(
			self.mouse_press_event, self.mouse_move_event, self.mouse_release_event
		)

		self.x_press = 0.0
		self.y_press = 0.0
		self.x_move = 0.0
		self.y_move = 0.0
		self.x_release = 0.0
		self.y_release = 0.0

		self.add_mouse_callbacks(mousePressEventCallback,mouseMoveEventCallback,mouseReleaseEventCallback)

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
		return self.two_points_to_rect_shape(self.x_press,self.y_press,self.x_move,self.y_move)
	
	def two_points_to_rect_shape(self,x1:float,y1:float,x2:float,y2:float):
		left, top, width, height = 0.0, 0.0, 0.0, 0.0

		x_press = x1
		y_press = y1
		x_move = x2
		y_move = y2

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


#########################################################################################
#########################################################################################
#########################################################################################

class ResizableRectItem(QGraphicsRectItem):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)
		self.setPen(QPen(QColor("red"), 1))
		self.setBrush(QColor(0, 0, 0, 0))

	def boundingRect(self):
		return QRectF(0, 0, 1920, 1080)


class NetworkRequestWorker(QRunnable):
	def __init__(self,url,data):
		super().__init__()
		self.url = url
		self.data = data

	def run(self):
		try:
			post_image(self.url, self.data)
		except KnownError:
			traceback.print_exc()
			print("Error has happened")

#########################################################################################
#########################################################################################
#########################################################################################

class ScreenCapturerApp(QWidget):
	def __init__(self,app:QApplication) -> None:
		super().__init__()

		# App
		self.app = app

		# Create graphics SCENE
		self.graphics_scene = GraphicsScene()
		self.mouse_handler = MouseHandler(self.graphics_scene, self.mouse_press_event, self.mouse_move_event, self.mouse_release_event)
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
		self.thread_pool = QThreadPool()
		
		self.screenCapturer = ScreenCapturerPyside()


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
		rect_shape = (left, top, width, height) = self.mouse_handler.mouse_positions_to_rect_shape()
		if width > 0 and height > 0:
			# print(self.mouse_handler.mouse_positions_to_rect_shape())
			self.cropped_pixmap = self.screenshot.copy(
				*rect_shape
			)
			selection_area = QGraphicsPixmapItem(self.cropped_pixmap)
			selection_area.setPos(left, top)

			selection_area2 = ResizableRectItem(
				*rect_shape
			)

			self.graphics_scene.removeItem(self.items[-1])
			self.graphics_scene.removeItem(self.items[-2])
			self.items.pop()
			self.items.pop()
			self.items.append(selection_area)
			self.items.append(selection_area2)
			self.graphics_scene.addItem(selection_area)
			self.graphics_scene.addItem(selection_area2)

	def mouse_release_event(self):
		captured_region = self.screenCapturer.convert_pixmap_to_bytes(self.cropped_pixmap)
		print("POSTING")
		
		worker = NetworkRequestWorker("http://localhost:54321",captured_region)
		self.thread_pool.start(worker)

		self.hide()

	def run(self):
		self.app.exec()

	def hide(self):
		self.main_window.hide()

	def delete(self):
		self.app.quit()
		self.app.exit(0)
		# signal.signal(signal.SIGINT, signal.SIG_DFL)
		QApplication.instance().quit() # type: ignore
		self.close()
		
		# app = QCoreApplication(sys.argv)
		# app.exec_()
		# sys.exit(0)

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

	def capture_region(self,two_points:TwoPoints):
		print("OBJECT OBJECT",two_points)

		# Get screenshot
		screen = QApplication.primaryScreen()
		screenshot = screen.grabWindow(0)

		# Get cropped screenshot
		cropped_pixmap = screenshot.copy(
			*self.mouse_handler.two_points_to_rect_shape(two_points.x1,two_points.y1,two_points.x2,two_points.y2)
		)

		screenshot_bytes = self.screenCapturer.convert_pixmap_to_bytes(cropped_pixmap)
		print("POSTING")
		
		worker = NetworkRequestWorker("http://localhost:54321",screenshot_bytes)
		self.thread_pool.start(worker)

#########################################################################################
#########################################################################################
#########################################################################################

class ScreenCapturerBase(ABC):
	@abstractmethod
	def capture_region(self):
		pass


class ScreenCapturerPyside(QObject):
	def __init__(self) -> None:
		super().__init__()

		self.latest_screenshot:None|QPixmap = None

	def get_latest_screenshot(self) -> QPixmap:
		if isinstance(self.latest_screenshot,QPixmap):
			return self.latest_screenshot
		else:
			raise Exception("ERROR: screenshot does not exist yet!")	

	def capture_region(self):
		# Get screenshot
		screen = QApplication.primaryScreen()
		screenshot = screen.grabWindow(0)

		# Load & Display Image
		image_item = QGraphicsPixmapItem(screenshot)
		image_item.setOpacity(0.88)
		##### image_item = QGraphicsPixmapItem(QPixmap("client/test2.png"))

		# self.graphics_scene.addItem(image_item)
		# self.items.append(image_item)
		
	def convert_pixmap_to_bytes(self,pixmap:QPixmap):
		buffer_array = QByteArray()

		buffer = QBuffer(buffer_array)
		buffer.open (QIODevice.OpenModeFlag.WriteOnly)

		ok = pixmap.save(buffer,"JPG")
		assert ok

		pixmap_bytes = buffer_array.data()
		return pixmap_bytes
	
#########################################################################################
#########################################################################################
#########################################################################################

class SignalHandler(QObject):
	signal = Signal(object)
	def __init__(self, parent: QObject|None = None) -> None:
		super().__init__(parent)
		self.signal.connect(self.signal_handler)
		
	def signal_handler(self,callback:Callable[...,None]):	# type: ignore
		callback()

#########################################################################################
#########################################################################################
#########################################################################################

if __name__ == "__main__":
	app = QApplication([])
	ocr_capture_app = ScreenCapturerApp(app)

	signal_handler = SignalHandler()

	thread_pool = QThreadPool()
	hotkey_runnable = HotkeyRunnable(
	[
		Hotkey(modifiers=[91],key=192,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.show())),
		Hotkey(modifiers=[],key=0x1B,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.hide())),
		Hotkey(modifiers=[91],key=0x90,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.delete())),
		Hotkey(modifiers=[91],key=0x5A,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=0,y1=0,x2=1920,y2=1080)))),
	])
	thread_pool.start(hotkey_runnable)

	print("Setup done!")
	
	ocr_capture_app.run()

"""
https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes 
asd
`
 """