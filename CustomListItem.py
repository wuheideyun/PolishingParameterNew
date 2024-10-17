'''

自定义列表项

图片32 * 32

item 高 32 + 5 * 2，
宽10 + 32 + 60 + 10 = 112

高 42 * 6

'''
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout


class CustomListItem(QWidget):
    # image_path: 图片路径
    # text: 文本
    def __init__(self, image_path, text):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        hLay = QHBoxLayout()
        self.setLayout(hLay)

        item_w = 172
        item_h = 42
        self.setFixedSize(item_w, item_h)

        self.labelLeft = QLabel(text, self)
        self.labelLeft.setFixedSize(32, 32)

        self.setStyleSheet('''
            QWidget {
                outline: none;              /* 去掉虚线框 */
                color: white;
                font-size: 14px;
                border: 0px solid transparent;
                background-color: transparent;
            }
        ''')

        # 加载图片并设置给 QLabel
        pixmap = QPixmap(image_path)  # 替换为实际图片路径
        self.labelLeft.setPixmap(pixmap)

        # 如果需要，可以让图片自适应 QLabel 的大小
        self.labelLeft.setScaledContents(True)

        self.labelRight = QLabel(text, self)
        self.labelRight.setFixedSize(70, 32)

        hLay.addWidget(self.labelLeft)
        hLay.addWidget(self.labelRight)

        self.setLayout(hLay)

    def setLabelName(self,name):
        self.labelRight.setText(name)


