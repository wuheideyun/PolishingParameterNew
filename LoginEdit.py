from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLineEdit, QLabel, QHBoxLayout


class LoginEdit(QLineEdit):
    def __init__(self, image_path):
        super().__init__()

        self.setFixedSize(326, 42)

        leftLabel = QLabel()
        label_w = 30
        leftLabel.setFixedSize(label_w, 30)

        pixmap = QPixmap(image_path)  # 替换为实际图片路径
        leftLabel.setPixmap(pixmap)

        # 如果需要，可以让图片自适应 QLabel 的大小
        leftLabel.setScaledContents(True)

        hlay = QHBoxLayout()
        hlay.addWidget(leftLabel)
        hlay.addStretch()

        left_diff = 7
        hlay.setContentsMargins(left_diff, 0, 0, 0)
        self.setTextMargins(label_w + left_diff + 5, 0, 5, 0)  # 距离右边为 5

        self.setStyleSheet("""
            QLineEdit {
                font-size: 13px;
                font-family: "Microsoft YaHei";
                border: none;  
                border-bottom: 1px solid rgb(200, 200, 200);  
            }
        """)

        self.setLayout(hlay)