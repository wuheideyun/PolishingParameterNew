from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QPoint, Qt, QEvent
import sys
import Resources

class ImageToolTip(QWidget):
    def __init__(self, image_path, parent=None, border_width=2, border_color="black"):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip)  # 让窗口成为悬浮气泡提示样式

        # 设置边框样式
        self.setStyleSheet(f"border: {border_width}px solid {border_color};")

        layout = QVBoxLayout()
        self.image_label = QLabel(self)

        # 加载图片
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def show_at_position(self, pos):
        """根据传入的位置调整气泡提示框显示的位置"""
        self.move(pos)
        self.show()


class HoverButton(QPushButton):
    def __init__(self, image_path, parent=None, border_width=0, border_color="white"):
        super().__init__('?', parent)  # 初始化按钮，默认显示“问号”

        # 创建气泡提示窗口，传入图片路径和边框信息
        self.tooltip = ImageToolTip(image_path, self, border_width, border_color)

        self.installEventFilter(self)  # 安装事件过滤器

    def eventFilter(self, source, event):
        # 监听鼠标进入和离开事件
        if event.type() == QEvent.Enter and source == self:
            # 设置提示框的位置（相对于按钮的显示位置，可以自行调整）
            pos = self.mapToGlobal(QPoint(-670, self.height()))  # 默认在按钮的下方中间显示
            self.tooltip.show_at_position(pos)
        elif event.type() == QEvent.Leave and source == self:
            self.tooltip.hide()

        return super(HoverButton, self).eventFilter(source, event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个自定义按钮，传入图片路径，边框宽度和颜色
        self.button = HoverButton(":keda", self, border_width=0, border_color="white")
        self.button.setGeometry(100, 100, 100, 40)  # 设置按钮位置

        self.setWindowTitle("Custom HoverButton Example")
        self.setGeometry(300, 300, 400, 300)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
