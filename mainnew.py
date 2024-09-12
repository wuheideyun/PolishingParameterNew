'''

主程序

'''

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from MainWindow import MainWindow
import Resources
from MainWindowNewImpl import MainWindowNewImpl

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(":writered"))

    w = MainWindow()
    rw = MainWindowNewImpl(w)
    w.show()

    sys.exit(app.exec())