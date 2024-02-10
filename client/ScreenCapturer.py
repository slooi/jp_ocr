import signal
import sys
import time
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, TypedDict, Union
from PySide6.QtCore import Qt, QRectF, QEvent, Signal, QObject, QThread, QByteArray, QIODevice, QBuffer, QRunnable, QThreadPool, QCoreApplication, QTimer, QPropertyAnimation
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

from main import KnownError, TwoPoints, NetworkHandler

from HotkeyHandler import Hotkey, WindowsHotkeyHandler
from abc import ABC, abstractmethod
import traceback
import pyperclip # type: ignore
import json

import ast
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

		# Container for items
		self.items_list = []


	# PUBLIC METHODS
	def add_items(self,*items:QGraphicsItem):
		for item in items:
			self.addItem(item)
			self.items_list.append(item)

	def clear_items(self):
		self.clear()
		self.items_list = []

	def remove_items(self,*items:QGraphicsItem):
		for item in items:
			try:
				self.removeItem(item)
				self.items_list.remove(item)
			except:
				# traceback.print_exc()
				print("Can't remove items! They probably don't exist anymore")


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

class ToolNotification(QLabel):
	def __init__(self,string:str):
		super().__init__(string)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
		self.setGeometry(1920-170,1080-50,170-10,50-10)
		self.hide()

		self.timer = QTimer()
		self.timer.setSingleShot(True)  # Set the timer to be a single shot (only fires once)
		self.timer.timeout.connect(self.startFadeOutAnimation)
		
		self.setStyleSheet(
			"""
			border: 1px solid white;
			margin: 4px;
			color: white;
			background-color: #404040;
		"""
		)

	def update_text(self, text_string: str):
		self.setWindowOpacity(0.85)

		self.setText(text_string)
		font = self.font()
		font.setBold(True)
		font.setPointSize(14)
		self.setFont(font)
		self.show()

		self.timer.start(2000)  # Start the timer to trigger the fade out animation after 3 seconds

	def startFadeOutAnimation(self):
		# Create a property animation for the opacity property
		self.animation = QPropertyAnimation(self, b"windowOpacity")
		self.animation.setDuration(1000)
		self.animation.setEndValue(0) # set end opacity = 0

		self.animation.start()


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Set hints
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		# self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

class MouseHandlerButtons(TypedDict):
	x_press: float
	y_press: float
	x_move: float
	y_move: float
	x_release: float
	y_release: float

class MouseHandler:
	def __init__(self, graphics_scene: GraphicsScene,
		mousePressEventCallback: Callable[[], None],
		mouseMoveEventCallback: Callable[[], None],
		mouseReleaseEventCallback: Callable[[], None]) -> None:
		graphics_scene.add_mouse_callbacks(
			self.mouse_press_event, self.mouse_move_event, self.mouse_release_event
		)

		self.buttons: Dict[Qt.MouseButton, MouseHandlerButtons] = {}
		self.intialize_mouse_buttons(Qt.MouseButton.LeftButton,Qt.MouseButton.RightButton,Qt.MouseButton.MiddleButton,Qt.MouseButton.NoButton)

		self.add_mouse_callbacks(mousePressEventCallback,mouseMoveEventCallback,mouseReleaseEventCallback)

	def intialize_mouse_buttons(self,*button_types):
		for button_type in button_types:
			self.buttons[button_type] = {
				"x_press": 0.0,
				"y_press": 0.0,
				"x_move": 0.0,
				"y_move": 0.0,
				"x_release": 0.0,
				"y_release": 0.0
			}

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
		print("press",event.buttons(),event.buttons().value,type(event.buttons().value),type(event.buttons()),dir(event.buttons()))
		self.buttons[event.buttons()]["x_press"] = event.scenePos().x()
		self.buttons[event.buttons()]["y_press"] = event.scenePos().y()

		self.buttons[event.buttons()]["x_move"] = event.scenePos().x()  # Slight hack.......
		self.buttons[event.buttons()]["y_move"] = event.scenePos().y()  # Slight hack.......
		self.mousePressEventCallback()

	def mouse_move_event(self, event: QGraphicsSceneMouseEvent):
		print("move",event.buttons(),event.buttons().value,type(event.buttons().value),type(event.buttons()),dir(event.buttons()))
		self.buttons[event.buttons()]["x_move"] = event.scenePos().x()
		self.buttons[event.buttons()]["y_move"] = event.scenePos().y()
		self.mouseMoveEventCallback()

	def mouse_release_event(self, event: QGraphicsSceneMouseEvent):
		print("release",event.buttons(),event.buttons().value,type(event.buttons().value),type(event.buttons()),dir(event.buttons()))
		self.buttons[event.buttons()]["x_release"] = event.scenePos().x()
		self.buttons[event.buttons()]["y_release"] = event.scenePos().y()
		self.mouseReleaseEventCallback()

	def get_press(self,mouse_button:Qt.MouseButton=Qt.MouseButton.LeftButton) -> Tuple[float,float]:
		return (self.buttons[mouse_button]["x_press"],self.buttons[mouse_button]["y_press"])
		
	def get_move(self,mouse_button:Qt.MouseButton=Qt.MouseButton.LeftButton) -> Tuple[float,float]:
		return (self.buttons[mouse_button]["x_move"],self.buttons[mouse_button]["y_move"])

	# PRIVATE METHODS
	def get_mouse_positions_in_rect_shape(self):
		left_button = self.buttons[Qt.MouseButton.LeftButton]
		return self.two_points_to_rect_shape(left_button["x_press"],left_button["x_press"],left_button["x_move"],left_button["y_move"])
	
	@staticmethod
	def two_points_to_rect_shape(x1:float,y1:float,x2:float,y2:float) -> Tuple[int,int,int,int]:
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

		return (round(left), round(top), round(width), round(height))


#########################################################################################
#########################################################################################
#########################################################################################

class ResizableRectItem(QGraphicsRectItem):
	def __init__(self, x, y, width, height,graphics_scene:GraphicsScene):
		super().__init__(x, y, width, height)
		self.setPen(QPen(QColor("red"), 1))
		self.setBrush(QColor(0, 0, 0, 0))

		self.graphics_scene = graphics_scene
		self.graphics_scene.add_items(self)

	def boundingRect(self):
		return QRectF(0, 0, 1920, 1080)


class NetworkRequestWorker(QRunnable):
	def __init__(self,url,data,callback:Callable[...,Any]|None = None): # type: ignore
		super().__init__()
		self.url = url
		self.data = data
		self.callback = callback

	def run(self):
		try:
			result = NetworkHandler.post_image(self.url, self.data)
			if self.callback:
				self.callback(result)
		except KnownError:
			traceback.print_exc()
			print("KnownError Error has happened")
		except pyperclip.PyperclipException:
			traceback.print_exc()
			print("PyperclipException Error has happened")


#########################################################################################
#########################################################################################
#########################################################################################

class HighlightedAreaItemManager():
	def __init__(self,x1,y1,x2,y2,full_screenshot:QPixmap,graphics_scene:GraphicsScene):
		self.graphics_scene = graphics_scene
		self.full_screenshot = full_screenshot
		self.highlighted_cropped_screenshot:None|QGraphicsPixmapItem = None
		self.cropped_screenshot:None|QPixmap = None

		# Get coordinates
		rect_shape  = MouseHandler.two_points_to_rect_shape(x1,y1,x2,y2)

		# Create highlighted area
		self.create_highlighted_area(*rect_shape)

	def create_highlighted_area(self,left:float,top:float,width:float,height:float):
		if width > 0 and height > 0:
			self.cropped_screenshot = self.full_screenshot.copy(*(int(left),int(top),int(width),int(height)))
		else:
			self.cropped_screenshot = self.full_screenshot.copy(*(0,0,1,1))

		self.highlighted_cropped_screenshot = QGraphicsPixmapItem(self.cropped_screenshot)
		self.highlighted_cropped_screenshot.setPos(left, top)
		self.graphics_scene.add_items(self.highlighted_cropped_screenshot)
		# Rectangle
		self.rectangle = ResizableRectItem(left,top,width,height,self.graphics_scene)


	def update(self,x1:float,y1:float,x2:float,y2:float):
		# Get coordinates
		rect_shape = MouseHandler.two_points_to_rect_shape(x1,y1,x2,y2)

		# Remove old
		if self.highlighted_cropped_screenshot: self.graphics_scene.remove_items(self.highlighted_cropped_screenshot)
		self.graphics_scene.remove_items(self.rectangle)

		# Create highlighted area
		self.create_highlighted_area(*rect_shape)

	def get_cropped_screenshot(self):
		if isinstance(self.cropped_screenshot,QPixmap): 
			return self.cropped_screenshot
		else:
			raise Exception("ERROR: self.cropped_screenshot doesn't exist yet!")


class ScreenCapturerApp(QWidget):
	notification_signal = Signal(str)
	def __init__(self,app:QApplication) -> None:
		super().__init__()

		# App
		self.app = app

		# Create graphics SCENE
		self.graphics_scene = GraphicsScene()
		self.mouse_handler = MouseHandler(self.graphics_scene, self.mouse_press_event, self.mouse_move_event, self.mouse_release_event)
		# Create VIEW from SCENE
		self.graphics_view = GraphicsView(self.graphics_scene)

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
		self.notification_signal.connect(self.notification)
		self.notification_widget = ToolNotification("")
		self.notification_widget.hide()
		self.screenCapturer = ScreenCapturerPyside()

	def mouse_press_event(self):
		pass

	def mouse_move_event(self):
		if not self.highlightedAreaItemManager: raise Exception("ERROR: self.highlightedAreaItemManager DOES NOT EXIST!")
		# print(self.mouse_handler.buttons)
		self.highlightedAreaItemManager.update(*self.mouse_handler.get_press(),*self.mouse_handler.get_move())

	def _image_post_response_callback(self,x):
		try:
			pyperclip.copy(x)
			self.notification_signal.emit("Text Copied")
		except:
			try:
				self.notification_signal.emit("ERROR: "+x["error"])
			except:
				raise Exception("ERROR: Did not except this to happen")
			
	def mouse_release_event(self):
		captured_region = self.screenCapturer.convert_pixmap_to_bytes(self.highlightedAreaItemManager.get_cropped_screenshot())
		print("POSTING")
		
		worker = NetworkRequestWorker("http://localhost:54321",captured_region,self._image_post_response_callback)
		self.thread_pool.start(worker)

		self.hide()
		
		
		# if not self.isHidden():

	def notification(self,text:str):
		self.notification_widget.update_text(text)

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

		
	def manual_region_capture(self):
		print("showing!")
		
		# 1) Remove any items from render
		self.graphics_scene.clear_items()

		# 2) Take screenshot
		screenshot = self.screenCapturer.capture_region()
		
		######################## graphics items ############################
		# 3) Display low opacity screenshot graphics item
		image_item = QGraphicsPixmapItem(screenshot)
		image_item.setOpacity(0.88)
		self.graphics_scene.add_items(image_item)
	
		# 4) Create border graphics item
		ResizableRectItem(0, 0, 1920-1, 1080-1,self.graphics_scene)

		# 5) Create bordered graphics item
		self.highlightedAreaItemManager = HighlightedAreaItemManager(0,0,0,0,screenshot,self.graphics_scene)

		# DISPLAY
		self.main_window.showFullScreen()
		self.main_window.raise_()

	def capture_region(self,two_points:TwoPoints):
		print("OBJECT OBJECT",two_points)

		# Get cropped screenshot
		cropped_screenshot = self.screenCapturer.capture_region(two_points)

		# Get cropped screenshot in byte form
		screenshot_bytes = self.screenCapturer.convert_pixmap_to_bytes(cropped_screenshot)

		# Post cropped screenshot
		print("POSTING")
		worker = NetworkRequestWorker("http://localhost:54321",screenshot_bytes,self._image_post_response_callback)
		self.thread_pool.start(worker)

#########################################################################################
#								SCREEN CAPTURER
#########################################################################################

class ScreenCapturerBase(ABC):
	@abstractmethod
	def capture_region(self):
		pass


class ScreenCapturerPyside(QObject):
	def __init__(self) -> None:
		super().__init__()

	def capture_region(self,two_points:TwoPoints|None = None):
		# Get screenshot
		screen = QApplication.primaryScreen()
		if isinstance(two_points,TwoPoints):
			screenshot = screen.grabWindow(0,*MouseHandler.two_points_to_rect_shape(two_points.x1,two_points.y1,two_points.x2,two_points.y2))
		else:
			screenshot = screen.grabWindow(0)

		return screenshot
	
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
	def debug_check():
		print("debug_check ran!")
		ocr_capture_app.manual_region_capture()
	def region_capture():
		print("region capture hotkey pressed")
		signal_handler.signal.emit(lambda:debug_check())
	thread_pool.start(HotkeyRunnable(
	[
		Hotkey(modifiers=[91],key=192,callback=lambda:region_capture()),
		# Hotkey(modifiers=[],key=0x1B,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.hide())),
		Hotkey(modifiers=[91],key=0x90,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.delete())),
		Hotkey(modifiers=[91],key=0x5A,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=960-450,y1=730,x2=960+450,y2=940)))),
	]))

	print("Setup done!")
	
	ocr_capture_app.run()

"""
https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes 
asd`	
``
 """