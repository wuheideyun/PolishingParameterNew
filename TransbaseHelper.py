from PySide6.QtCore import QTranslator, QCoreApplication
from PySide6.QtWidgets import QApplication


class TransbaseHelper2:
    def __init__(self):
        self.current_language = "zh"
        self.translator = QTranslator()
        self.translator.load("zh_CN.qm")


    def ChangeLanguage(self, isChinese):
        if isChinese:
            self.current_language = "zh"
            QApplication.instance().removeTranslator(self.translator)
        else:
            self.current_language = "en"
            QApplication.instance().installTranslator(self.translator)

    def getTransText(self,textname):
        return QCoreApplication.translate("MainWindow",textname,None)