import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.setWindowTitle("Simple Text Editor")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())
