from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication
# 创建翻译器
translator = QTranslator()
# 加载翻译文件
translator.load("zh_CN.qm")
# 安装翻译器
QApplication.installTranslator(translator)