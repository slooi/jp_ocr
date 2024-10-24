
from HotkeyHandler import Hotkey
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QApplication
from ScreenCapturer import HotkeyRunnable, ScreenCapturerApp, SignalHandler
from utils import TwoPoints

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
		
	LEFT_ALT_KEY = 0xA4
	LEFT_CONTROL_KEY = 0xA2
	LEFT_SHIFT_KEY = 0xA0
	LEFT_WIN_KEY = 91
	A_KEY = 0x41
	Z_KEY = 0x5A
	S_KEY = 0x53
	thread_pool.start(HotkeyRunnable(
	[
		Hotkey(modifiers=[LEFT_WIN_KEY],key=192,callback=lambda:region_capture()),
		# Hotkey(modifiers=[],key=0x1B,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.hide())),
		Hotkey(modifiers=[LEFT_WIN_KEY],key=0x90,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.delete())),
		
		# BP
		# Hotkey(modifiers=[LEFT_WIN_KEY],key=0x5A,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=960-450,y1=730,x2=960+450,y2=940)))),
	

	
		# GRANBLUE FANTASY - DIALOGUE (does capture name)
		Hotkey(modifiers=[LEFT_WIN_KEY],key=Z_KEY,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=450,y1=717,x2=960+450,y2=1040)))),
		# GRANBLUE FANTASY - DIALOGUE (doesn't capture name)
		# Hotkey(modifiers=[LEFT_WIN_KEY],key=Z_KEY,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=960-450,y1=875,x2=960+450,y2=1040)))),
		
		# GRANBLUE FANTASY - POPUP HEADER
		Hotkey(modifiers=[LEFT_ALT_KEY,LEFT_CONTROL_KEY],key=A_KEY,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=460,y1=195,x2=1461,y2=280)))),
		# GRANBLUE FANTASY - POPUP CONTENT
		Hotkey(modifiers=[LEFT_ALT_KEY,LEFT_CONTROL_KEY],key=Z_KEY,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=459,y1=606,x2=1460,y2=788)))),

		# GRANBLUE FANTASY - CHOOSE DIALOGUE CENTER
		Hotkey(modifiers=[LEFT_ALT_KEY,LEFT_CONTROL_KEY],key=S_KEY,callback=lambda:signal_handler.signal.emit(lambda:ocr_capture_app.capture_region(TwoPoints(x1=568,y1=340,x2=1345,y2=606)))),
	]))

	print("Setup done!")
	ocr_capture_app.run()