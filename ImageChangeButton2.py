'''

自定义图片按钮类

'''
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QFontMetrics, QPixmap
from PySide6.QtWidgets import QPushButton


class ImageChangeButton2(QPushButton):
    def __init__(self,text, image_path1,image_path2, fixed_w, fixed_h):
        super().__init__()
        self.text = text
        self.setFixedSize(fixed_w, fixed_h)

        self.setText("")  # 设置按钮文字
        self.setIcon(QIcon(image_path1))  # 设置按钮图标

        self.pixmap = QPixmap(image_path1)
        # 让图标自适应按钮大小
        # self.setIconSize(self.size())  # 和按钮的尺寸一致
        self.setIconSize(QSize(300,100))  # 和按钮的尺寸一致
        self.setStyleSheet("""
            QPushButton {
                border: none; /* 无边框 */
            }

            QPushButton:hover {
                background-color: grey; /* 鼠标悬停时的背景色 */
            }

            QPushButton:pressed {
                background-color: #aaaaaa; /* 鼠标按下时的背景色 */
            }
        """)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

        # 设置字体大小
        font = self.font()
        font.setPointSize(16)  # 将字体大小设置为16
        painter.setFont(font)

        # 设置文字颜色
        painter.setPen(Qt.white)

        # 获取字体度量对象
        font_metrics = QFontMetrics(font)

        # 获取文字的宽度和高度
        text_width = font_metrics.horizontalAdvance(self.text)
        text_height = font_metrics.height()

        # 计算文字的 x, y 坐标，使其居中显示
        x = (self.width() - text_width) / 2
        y = (self.height() + text_height) / 2 - text_height / 4

        painter.drawText(x, y, self.text)