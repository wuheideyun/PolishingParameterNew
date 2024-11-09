from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QLabel, QVBoxLayout, QGroupBox, \
    QLineEdit, QHBoxLayout
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("填充背景图片")

        # 初始窗口大小
        self.resize(960, 540)

        # 设置背景图片路径
        self.background_image_path = "./Resources/NewUI/Base/background.png"
        self.background_image = QPixmap(self.background_image_path)

        # 设置背景
        self.update_background_image()







    def set_background_image(self):
        # 将图片缩放至窗口大小，不保持纵横比，填充满整个窗口
        window_size = self.size()
        scaled_image = self.background_image.scaled(window_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # 设置为窗口背景
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_image))
        self.setPalette(palette)

    def update_background_image(self):
        # 更新背景图片的显示效果
        self.set_background_image()

    def resizeEvent(self, event):
        # 窗口大小改变时更新背景图片
        self.update_background_image()

        # 继承父类的 resizeEvent
        super(MainWindow, self).resizeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
