'''

自定义图片按钮类

'''
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap, QPalette, QBrush, QPainter, QFontMetrics
from PySide6.QtWidgets import QPushButton


class ImageChangeWithTextButton(QPushButton):
    def __init__(self, text, image_path,image_path2, fixed_w, fixed_h ,parent=None):
        super().__init__(parent)
        self.setFixedSize(fixed_w, fixed_h)
        self.text = text
        self.image_path = image_path
        self.pixmap = QPixmap(image_path)
        self.setStyleSheet("""
                                    QPushButton {
                                        border: none; /* 无边框 */
                                    }

                                    QPushButton:hover {
                                        background-color: red; /* 鼠标悬停时的背景色 */
                                    }

                                    QPushButton:pressed {
                                        background-color: #aaaaaa; /* 鼠标按下时的背景色 */
                                    }
                                """)
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)





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
