import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from MainWindow_new_impl import MainWindow_impl
import Resources
import Resources_Device

global_style = """
    QMessageBox {
        background-color: rgb(31, 55, 96);
    }
    QMessageBox QLabel {
        color: white;
        font-family: "Microsoft YaHei"; /* 字体样式 */
        font-size: 18px; /* 字体大小 */
    }
    QMessageBox QWidget#qt_msgbox_label {
        font-family: "Microsoft YaHei"; /* 标题字体样式 */
        font-size: 18px; /* 标题字体大小 */
        color: white; /* 标题颜色 */
    }
    QMessageBox QPushButton {
        background-color: #444;
        color: white;
        border: 1px solid #555;
        padding: 5px 10px;
    }
    QMessageBox QPushButton:hover {
        background-color: #555;
    }
    """
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 启用高 DPI 缩放支持
    # app.setAttribute(Qt.AA_EnableHighDpiScaling)
    # app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # app = QApplication(sys.argv)
    app.setStyleSheet("QHeaderView::section { color: white; }")  # 全局强制设置表头文本颜色
    # 设置全局样式（可选）
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(":writered"))
    # 设置全局样式表
    app.setStyleSheet(global_style)
    w = MainWindow_impl()
    w.show()

    sys.exit(app.exec())