import time
from typing import Callable, List
from PySide6.QtCore import Qt, QRectF, Signal, QObject, QThread
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
			border: 1px solid #AA0000;
			background-color: black;
		"""
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set hints
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


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

    def __init__(self):
        super().__init__()
        print("Set triggers!")
        keyboard.add_hotkey("ctrl+g", self.hide.emit)
        keyboard.add_hotkey("ctrl+h", self.show.emit)


class ScreenCapturer:
    def __init__(self) -> None:
        # App
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
        self.setup()

        # Create main window
        self.main_window = MainWindow()
        self.main_window.setWindowTitle("OCR")
        self.main_window.setCentralWidget(self.graphics_view)

        # self.main_window.showFullScreen()
        # self.main_window.show()
        self.main_window.hide()

        # Register the hotkey (Ctrl+G) to show/hide the main window

        #############################
        # ADD THREAD AND SIGNALLER
        self._thread = QThread(self.main_window)

        self.signaller_worker = ScreenCapturerSignaller()
        self.signaller_worker.moveToThread(self._thread)

        self.signaller_worker.hide.connect(self.hide)
        self.signaller_worker.show.connect(self.show)

    def setup(self):
        self.add_screenshot()
        self.add_rectangle_SETUP()

    def add_screenshot(self):
        # Get screenshot
        screen = QApplication.primaryScreen()
        self.screenshot = screen.grabWindow(0)

        # Apply brightness adjustment
        # brightness_factor = 0.8
        # brightness_effect = QGraphicsColorizeEffect()
        # brightness_effect.setColor("#FFF")

        # Load & Display Image
        image_item = QGraphicsPixmapItem(self.screenshot)
        image_item.setOpacity(0.94)
        # image_item = QGraphicsPixmapItem(QPixmap("client/test2.png"))

        self.graphics_scene.addItem(image_item)
        self.items.append(image_item)

        # self.graphics_scene.removeItem(image_item)

    def add_rectangle_SETUP(self):
        if not self.screenshot:
            raise Exception("self.screenshot must be assigned first!")
        # Create selection area
        self.selection_area = ResizableRectItem(0, 0, 50, 50)

        # Add the item to the scene
        self.graphics_scene.addItem(self.selection_area)
        self.items.append(self.selection_area)

    def mouse_press_event(self):
        self.selection_area.setRect(*self.mouse_handler.mouse_positions_to_rect_shape())

    def mouse_move_event(self):
        self.selection_area.setRect(*self.mouse_handler.mouse_positions_to_rect_shape())

    def mouse_release_event(self):
        # self.show()
        # print("NAI WAH!")
        pass

    def run(self):
        self.app.exec()

    def hide(self):
        self.main_window.hide()

    def show(self):
        # self.main_window.show()
        # self.main_window.showMaximized()
        # self.main_window.setWindowState(Qt.WindowState.WindowMaximized)
        self.main_window.showFullScreen()


if __name__ == "__main__":
    ocr_capture_app = ScreenCapturer()
    ocr_capture_app.run()
