import sys
from PySide6.QtCore import QTranslator, QLocale, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

from SwitchButton import SwitchButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Language Switcher")

        # 创建界面元素
        self.label = QLabel(self.tr("Hello, World!"), self)
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton(self.tr("Switch to Chinese"), self)
        self.button.clicked.connect(self.switch_language)
        self.btn = SwitchButton()
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 初始化翻译器
        self.translator = QTranslator()
        self.current_language = "en"  # 初始语言为英文

    def switch_language(self):
        if self.current_language == "en":
            # 切换到中文
            if self.translator.load("zh_CN.qm"):  # 加载语言文件
                app.installTranslator(self.translator)
                self.label.setText(self.tr("Hello, World!"))
                self.button.setText(self.tr("Switch to English"))
                self.current_language = "zh"
        else:
            # 切换到英文
            app.removeTranslator(self.translator)
            self.label.setText("Hello, World!")
            self.button.setText("Switch to Chinese")
            self.current_language = "en"

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
