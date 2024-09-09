'''

自定义弹出式消息框

'''
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout

from FrameLessDialog import FrameLessDialog
from ImageButton import ImageButton


class PopupMessageBox(FrameLessDialog):
    def __init__(self, title = '提示', message = ''):
        super().__init__()

        self.resize(400, 200)

        self.title = title
        self.message = message

        mainVLay = QVBoxLayout()

        self.labelTitle = QLabel()
        self.labelTitle.setText(title)
        self.btnClose = ImageButton(":close16", 16, 16)
        self.btnClose.clicked.connect(self.close)

        hlay1 = QHBoxLayout()
        hlay1.addWidget(self.labelTitle)
        hlay1.addStretch()
        hlay1.addWidget(self.btnClose)

        mainVLay.addLayout(hlay1)

        self.labelMessage = QLabel()
        self.labelMessage.setAlignment(Qt.AlignCenter)  # 将文本居中对齐
        self.labelMessage.setText(message)

        hlay2 = QHBoxLayout()
        hlay2.addWidget(self.labelMessage)

        self.labelMessage.setStyleSheet('''
            QLabel {
                font-size: 20px;
                color: #000000;
            }
        ''')

        mainVLay.addLayout(hlay2)

        self.setLayout(mainVLay)

    def setTitle(self, title):
        self.labelTitle.setText(title)

    def setMessage(self, message):
        self.labelMessage.setText(message)



