'''

自定义图片文本按钮类

'''

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class ImageTextButton(QPushButton):

    # image_path: 图片路径
    # str: 按钮文字
    # fix_w: 按钮固定宽度
    # fix_h: 按钮固定高度
    def __init__(self, image_path, str, fix_w = 32, fix_h = 32):
        super().__init__()

        self.setFixedSize(fix_w, fix_h)
        self.setText(str)  # 设置按钮文字
        self.setIcon(QIcon(image_path))  # 设置按钮图标

        self.setStyleSheet("""
            QPushButton {
                text-align: left; /* 文字左对齐 */
                border: none; /* 无边框 */
            }
            
            QPushButton:hover {
                background-color: #cccccc; /* 鼠标悬停时的背景色 */
            }
            
            QPushButton:pressed {
                background-color: #aaaaaa; /* 鼠标按下时的背景色 */
            }
        """)

        # 让图标显示在文字左侧
        self.setLayoutDirection(Qt.LeftToRight)
