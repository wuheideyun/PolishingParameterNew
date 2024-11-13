'''

主程序

'''

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from MainWindow_New_Interface import MainWindow
from MainWindow_new_impl import MainWindow_impl
import Resources


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(":writered"))

    w = MainWindow_impl()
    w.show()

    sys.exit(app.exec())