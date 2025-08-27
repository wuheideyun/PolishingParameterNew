from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt


class ReadWriteWidget(QWidget):
    """一个包含只读'读取值'和可编辑'写入值'的自定义控件"""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(5)

        self.read_label = QLineEdit(self)
        self.read_label.setReadOnly(True)
        self.read_label.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")

        self.write_edit = QLineEdit(self)
        self.write_edit.setStyleSheet("background-color: white; color: black;")  # 写入框用白色背景以区分

        layout.addWidget(self.read_label)
        layout.addWidget(self.write_edit)