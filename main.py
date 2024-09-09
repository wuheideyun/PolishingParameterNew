'''

主程序

'''

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow
import Resources


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(":writered"))

    w = MainWindow()
    w.show()

    sys.exit(app.exec())