'''

自定义图片按钮类

'''

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class ImageButton(QPushButton):
    def __init__(self, image_path, fixed_w, fixed_h):
        super().__init__()

        self.setFixedSize(fixed_w, fixed_h)

        self.setText("")  # 设置按钮文字
        self.setIcon(QIcon(image_path))  # 设置按钮图标

        # 让图标自适应按钮大小
        self.setIconSize(self.size())  # 和按钮的尺寸一致

        self.setStyleSheet("""
            QPushButton {
                border: none; /* 无边框 */
            }

            QPushButton:hover {
                background-color: #f00; /* 鼠标悬停时的背景色 */
            }

            QPushButton:pressed {
                background-color: #aaaaaa; /* 鼠标按下时的背景色 */
            }
        """)



