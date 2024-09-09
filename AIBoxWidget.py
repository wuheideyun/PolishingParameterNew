'''

10 + 32 + 60 + 10

'''

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPalette, QColor, QPainter
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QCheckBox, QMessageBox


class AIBoxWidget(QWidget):

    sig_runse0 = Signal()

    def __init__(self):
        super(AIBoxWidget, self).__init__()

        self.setMouseTracking(True)

        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        mainHLayout = QHBoxLayout()

        item_w = 122
        item_h = 50

        self.setFixedSize(item_w, item_h)

        self.labelLeft = QLabel("", self)
        self.labelLeft.setFixedSize(32, 32)

        image_path = ":AI"

        # 加载图片并设置给 QLabel
        pixmap = QPixmap(image_path)  # 替换为实际图片路径
        self.labelLeft.setPixmap(pixmap)

        # 如果需要，可以让图片自适应 QLabel 的大小
        self.labelLeft.setScaledContents(True)

        mainHLayout.addWidget(self.labelLeft)

        # 设置垂直布局
        vlay = QVBoxLayout()

        # 添加一个按钮
        self.checkboxTop = QCheckBox("", self)
        self.checkboxTop.setFixedSize(75, 18)

        qss = '''
            QCheckBox::indicator:unchecked{ 
                image:url(:CkClose); 
            } 
            QCheckBox::indicator:checked { 
                image: url(:CkOpen); 
            }
        '''

        self.checkboxTop.setStyleSheet(qss)

        roundedButtonStyle = """
                    QPushButton {
                        background-color: rgb(220,160,210);
                        border-style: solid;
                        border-color: rgb(255,216,188);
                        border-width: 0px;
                        border-radius: 10px;
                        color: white;
                        padding: 5px;
                    }

                    QPushButton:pressed {
                        background-color: rgb(105,216,188);
                    }

                    QPushButton:hover {
                        background-color: rgb(200,160,210);
                    }
                """

        self.btnBottom = QPushButton("智能润色", self)
        self.btnBottom.setFixedSize(75, 22)
        self.btnBottom.setStyleSheet(roundedButtonStyle)
        self.btnBottom.clicked.connect(self.onRunse)

        # 将标签和按钮添加到布局中
        vlay.addWidget(self.checkboxTop)
        vlay.addWidget(self.btnBottom)

        mainHLayout.addLayout(vlay)

        mainHLayout.addStretch()

        self.setLayout(mainHLayout)

        self.enterWidget = False

    def onRunse(self):
        self.sig_runse0.emit()
        # QMessageBox.information(None, 'aibox', '智能润色')

    def enterEvent(self, event):
        qss = '''
            QCheckBox{
                background-color: rgb(201, 245, 255);
                border: none;
            }
            
            QCheckBox::indicator:unchecked{ 
                image:url(:CkClose); 
            } 
            QCheckBox::indicator:checked { 
                image: url(:CkOpen); 
            }
        '''

        self.checkboxTop.setStyleSheet(qss)

        # 鼠标进入窗口时改变背景色
        self.enterWidget = True
        self.update()
        event.accept()  # 标记事件已处理

    def leaveEvent(self, event):
        qss = '''
                    QCheckBox{
                        background-color: rgb(251, 245, 255);
                        border: none;
                    }

                    QCheckBox::indicator:unchecked{ 
                        image:url(:CkClose); 
                    } 
                    QCheckBox::indicator:checked { 
                        image: url(:CkOpen); 
                    }
                '''

        self.checkboxTop.setStyleSheet(qss)

        # 鼠标离开窗口时改变背景色
        self.enterWidget = False
        self.update()
        event.accept()  # 标记事件已处理

    def paintEvent(self, event):
        painter = QPainter(self)
        # 251,245,255

        if self.enterWidget:
            painter.fillRect(self.rect(), QColor(201, 245, 255))  # 使用QColor设置颜色
        else:
            painter.fillRect(self.rect(), QColor(251, 245, 255))  # 使用QColor设置颜色