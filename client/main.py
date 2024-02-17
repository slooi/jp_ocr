
from HotkeyHandler import Hotkey
from ScreenCapturer import HotkeyRunnable, ScreenCapturerApp, SignalHandler
from utils import TwoPoints

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
	app = QApplication([])	# Refactor this later into a class
	ocr_capture_app = ScreenCapturerApp(app)

	signal_handler = SignalHandler()

	thread_pool = QThreadPool()	# Refactor this later into a class
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
		
		# BP
		# Hotkey(modifiers=[91],key=0x5A,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=960-450,y1=730,x2=960+450,y2=940)))),
	
		# Granblue
		# mouse_x,mouse_y: 1480 1040
		# mouse_x,mouse_y: 480 810
		Hotkey(modifiers=[91],key=0x5A,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=480,y1=810,x2=1480,y2=1040)))),

	]))

	print("Setup done!")
	ocr_capture_app.run()