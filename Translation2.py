import sys
from PySide6.QtCore import QTranslator, QLocale, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Main Window"))

        # 创建界面元素
        self.label = QLabel(self.tr("Hello, World!"), self)
        self.label.setAlignment(Qt.AlignCenter)

        # self.statusBar().showMessage(self.tr("Ready"))
        # self.setup_menu()

        # 初始化翻译器
        self.translator = QTranslator()
        self.current_language = "en"  # 初始语言为英文

        self.retranslate_ui()  # 初始时加载界面翻译

    def setup_menu(self):
        # 创建菜单栏和工具栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu(self.tr("File"))

        switch_language_action = QAction(self.tr("Switch Language"), self)
        switch_language_action.triggered.connect(self.switch_language)
        file_menu.addAction(switch_language_action)

    def retranslate_ui(self):
        # 重新翻译所有需要动态更新的界面元素
        self.setWindowTitle(self.tr("Main Window"))
        self.label.setText(self.tr("保存参数"))
        self.statusBar().showMessage(self.tr("Ready"))

        # 更新菜单栏
        menubar = self.menuBar()
        menubar.clear()  # 清空旧菜单
        self.setup_menu()

    def switch_language(self):
        if self.current_language == "en":
            # 切换到中文
            if self.translator.load("zh_CN.qm"):  # 加载语言文件
                app.installTranslator(self.translator)
                self.current_language = "zh"
        else:
            # 切换到英文
            app.removeTranslator(self.translator)
            self.current_language = "en"

        self.retranslate_ui()  # 更新UI上的文字

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
