from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow



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
		self.setCentralWidget(self.label)
		# self.label.setPixmap(QPixmap("client/test.jpg"))


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
