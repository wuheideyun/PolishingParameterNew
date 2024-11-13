import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建中央窗口小部件和布局
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # 创建内容部件
        content = QLabel("这是一个很长的内容。\n" * 50)
        scroll_area.setWidget(content)

        # 自定义滚动条样式
        scroll_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                border: 1px solid #999999;
                background: #f0f0f0;
                width: 16px;
                margin: 16px 0 16px 0;
            }
            QScrollBar::handle:vertical {
                background: #5d99c6;
                min-height: 20px;
                border-radius: 8px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #e0e0e0;
            }
        """)

        scroll_area.horizontalScrollBar().setStyleSheet("""
            QScrollBar:horizontal {
                border: 1px solid #999999;
                background: #f0f0f0;
                height: 16px;
                margin: 0px 16px 0px 16px;
            }
            QScrollBar::handle:horizontal {
                background: #5d99c6;
                min-width: 20px;
                border-radius: 8px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: #e0e0e0;
            }
        """)

        # 添加滚动区域到布局中
        layout.addWidget(scroll_area)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
