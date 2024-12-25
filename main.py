import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from MainWindow_new_impl import MainWindow_impl
import Resources

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

    app.setWindowIcon(QIcon(":writered"))
    # 设置全局样式表
    app.setStyleSheet(global_style)
    w = MainWindow_impl()
    w.show()

    sys.exit(app.exec())