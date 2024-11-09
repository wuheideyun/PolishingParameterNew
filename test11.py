import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QFontMetrics
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout


class CustomButton(QPushButton):
    def __init__(self, text, image_path, parent=None):
        super().__init__(parent)
        self.text = text
        self.image_path = image_path
        self.pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

        # 设置文字颜色
        painter.setPen(Qt.white)
        # 获取字体度量对象
        font_metrics = QFontMetrics(self.font())
        # 获取文字的宽度和高度
        text_width = font_metrics.horizontalAdvance(self.text)
        text_height = font_metrics.height()
        # 计算文字的 x, y 坐标，使其居中显示
        x = (self.width() - text_width) / 2
        y = (self.height() + text_height) / 2 - text_height / 4
        painter.drawText(x, y, self.text)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = QWidget()
    layout = QVBoxLayout()

    button1 = CustomButton("按钮1", "./Resources/NewUI/Button/Small.png")

    layout.addWidget(button1)

    widget.setLayout(layout)
    widget.show()

    sys.exit(app.exec())