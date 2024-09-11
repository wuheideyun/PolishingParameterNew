from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QMessageBox

class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        #
        # # 设置对话框标题和大小
        # self.setWindowTitle("确认")
        # self.setFixedSize(200, 100)
        #
        # # 创建确认按钮
        # self.confirm_button = QPushButton("确认", self)
        # self.confirm_button.clicked.connect(self.confirm_action)
        self.confirm_action()
        #
        # # 布局
        # layout = QVBoxLayout(self)
        # layout.addWidget(self.confirm_button)
        # self.setLayout(layout)

    def confirm_action(self):
        """弹出确认对话框"""
        reply = QMessageBox.question(self, "确认", "你确定要退出登录吗？",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.accept()  # 确认操作
        else:
            self.reject()  # 取消操作