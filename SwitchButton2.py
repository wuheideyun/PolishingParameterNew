import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox

class LanguageSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Language Switcher')
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()

        self.language_combo = QComboBox(self)
        self.language_combo.addItem("English")
        self.language_combo.addItem("中文")
        self.language_combo.currentIndexChanged.connect(self.switchLanguage)

        self.switch_button = QPushButton('Switch Language', self)
        self.switch_button.clicked.connect(self.toggleLanguage)

        layout.addWidget(self.language_combo)
        layout.addWidget(self.switch_button)

        self.setLayout(layout)

    def switchLanguage(self):
        # 这里仅打印当前选择的语言，实际使用时可以在这里添加代码来切换应用的语言
        print(self.language_combo.currentText())

    def toggleLanguage(self):
        # 简单地切换下拉列表中的语言选项，实际使用时需要替换为实际的语言切换逻辑
        current_index = self.language_combo.currentIndex()
        self.language_combo.setCurrentIndex((current_index + 1) % self.language_combo.count())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LanguageSwitcher()
    ex.show()
    sys.exit(app.exec())
