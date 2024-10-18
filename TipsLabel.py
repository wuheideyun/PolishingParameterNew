from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QPoint, Qt, QEvent
import sys
import Resources

class ImageToolTip(QWidget):
    def __init__(self, image_path, parent=None, border_width=2, border_color="black"):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip)  # 让窗口成为悬浮气泡提示样式
        self.image_path =image_path
        # 设置边框样式
        self.setStyleSheet(f"border: {border_width}px solid {border_color};")

        layout = QVBoxLayout()
        self.image_label = QLabel(self)

        # 加载图片
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        self.load_and_scale_pixmap()  # 设置为显示 PNG 图片
        self.setLayout(layout)
    def load_and_scale_pixmap(self):
        """加载并缩放图片以适应标签宽度"""
        pixmap = QPixmap(self.image_path)
        # 计算高度以保持宽高比
        height = int((pixmap.height() / pixmap.width()) * 800)
        self.image_label.setPixmap(pixmap.scaled(800, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # 按比例缩放

        self.setFixedHeight(height)  # 设置标签高度
    def show_at_position(self, pos):
        """根据传入的位置调整气泡提示框显示的位置"""
        self.move(pos)
        self.show()


class HoverLabel(QLabel):
    def __init__(self, image_path, parent=None, border_width=0, border_color="white"):
        super().__init__('', parent)  # 初始化标签，默认显示“问号”
        self.image_path = image_path  # 保存图片路径
        # 创建气泡提示窗口，传入图片路径和边框信息
        self.tooltip = ImageToolTip(image_path, self, border_width, border_color)
        self.setAlignment(Qt.AlignCenter)  # 设置文本居中
        self.setPixmap(QPixmap(":tips"))
        # self.setStyleSheet("background-color: white;")  # 设置背景颜色，模拟按钮效果
        self.setFixedSize(22, 22)  # 设置标签固定大小
        self.setScaledContents(True)  # 允许缩放内容

        self.installEventFilter(self)  # 安装事件过滤器



    def eventFilter(self, source, event):
        # 监听鼠标进入和离开事件
        if event.type() == QEvent.Enter and source == self:
            # 设置提示框的位置（相对于标签的显示位置，可以自行调整）
            pos = self.mapToGlobal(QPoint(-760, self.height()))  # 默认在标签的下方中间显示
            self.tooltip.show_at_position(pos)
        elif event.type() == QEvent.Leave and source == self:
            self.tooltip.hide()

        return super(HoverLabel, self).eventFilter(source, event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个自定义标签，传入图片路径，边框宽度和颜色
        self.label = HoverLabel(":tips1", self, border_width=0, border_color="white")
        self.label.setGeometry(100, 100, 100, 40)  # 设置标签位置

        self.setWindowTitle("Custom HoverLabel Example")
        self.setGeometry(300, 300, 400, 300)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
