import sys

from PySide6.QtWidgets import QApplication

from FormOmron import FormOmron

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = FormOmron()
    w.show()

    sys.exit(app.exec())