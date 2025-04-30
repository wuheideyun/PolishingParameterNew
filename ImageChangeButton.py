'''
自定义图片按钮类
'''
from PySide6.QtCore import QSize, Qt, QEvent, QTimer
from PySide6.QtGui import QIcon, QPainter, QFontMetrics, QPixmap, QColor, QBrush
from PySide6.QtWidgets import QPushButton


class ImageChangeButton(QPushButton):
    def __init__(self, text, image_path1, image_path2, fixed_w, fixed_h,immediate_recovery = False):
        super().__init__()
        self.text = text
        self.setFixedSize(fixed_w, fixed_h)
        self.original_width = fixed_w  # 保存原始宽度
        self.current_width = fixed_w  # 当前宽度
        # 初始化标志位
        self.is_clicked = False  # 用于判断是否被点击
        self.image_path1 = image_path1
        self.image_path2 = image_path2
        self.immediate_recovery = immediate_recovery
        self.current_image_path = image_path1

        self.setText("")  # 设置按钮文字
        self.setIcon(QIcon(self.current_image_path))  # 设置按钮图标

        self.pixmap = QPixmap(self.current_image_path)
        self.setIconSize(QSize(fixed_w, fixed_h))  # 和按钮的尺寸一致
        self.setStyleSheet("""
            QPushButton {
                border: none; /* 无边框 */
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50); /* 鼠标悬停时的背景色，半透明白色 */
            }

            QPushButton:pressed {
                background-color: rgba(170, 170, 170, 50); /* 鼠标按下时的背景色，半透明灰色 */
            }
        """)

        # 连接点击事件
        self.clicked.connect(self.on_clicked)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.pixmap)

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

    def enterEvent(self, event):
        """鼠标进入按钮区域时，增加提亮效果"""
        if self.immediate_recovery or not self.is_clicked:
            # 增加提亮效果
            self.pixmap = self._get_brightened_pixmap(self.image_path1)
            self.update()

    def leaveEvent(self, event):
        pass
        """鼠标离开按钮区域时，恢复正常背景"""
        if self.immediate_recovery or not self.is_clicked :
            # 恢复正常背景
            self.pixmap = QPixmap(self.image_path1)
            self.update()

    def on_clicked(self):
        self.is_clicked = True
        # 点击按钮时切换背景图为 image_path2
        self.current_image_path = self.image_path2
        self.pixmap = QPixmap(self.current_image_path)
        self.update()
        if self.immediate_recovery:
            QTimer.singleShot(100, self.on_timer_timeout)


    def on_timer_timeout(self):
        # 1000 毫秒后执行的代码
        self.reset_background()

    # def mouseReleaseEvent(self, event):
    #     """鼠标松开时，根据immediate_recovery 参数决定是否恢复背景图为 image_path1"""
    #     if self.immediate_recovery:
    #         # self.reset_background()
    #         print('aaa')

    def _get_brightened_pixmap(self, image_path):
        """增加图像的亮度"""
        original_pixmap = QPixmap(image_path)
        brightened_pixmap = QPixmap(original_pixmap.size())
        brightened_pixmap.fill(Qt.transparent)

        painter = QPainter(brightened_pixmap)
        painter.setOpacity(0.5)  # 设置亮度效果，值越大越亮
        painter.drawPixmap(0, 0, original_pixmap)
        painter.end()

        return brightened_pixmap
    def reset_background(self):
        # 重置背景图为 image_path1
        self.current_image_path = self.image_path1
        self.pixmap = QPixmap(self.current_image_path)
        self.update()
        self.is_clicked = False

    def init_clicked_background(self):
        # 重置背景图为 image_path1
        self.current_image_path = self.image_path2
        self.pixmap = QPixmap(self.current_image_path)
        self.update()

    def set_name(self, newName):
        self.text = newName

        # 获取字体度量，计算文本宽度
        font = self.font()
        font.setPointSize(16)  # 与 paintEvent 一致
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(newName)

        # 计算新宽度：文本宽度 + 边距（例如 20 像素）
        padding = 20
        new_width = max(self.original_width, text_width + padding)

        # 如果文本宽度超过当前宽度，动态调整按钮宽度
        if new_width != self.current_width:
            self.current_width = new_width
            self.setFixedSize(new_width, self.height())
            self.setIconSize(QSize(new_width, self.height()))  # 同步图标大小

        self.update()  # 触发重绘