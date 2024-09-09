'''

中间内容控件

'''
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QStyleOption, QStyle, QMainWindow

from Double_Calc_WidgetImpl import DoubleCalcWidgetImpl
from Double_Sim_WidgetImpl import DoubleSimWidgetImpl
from Equal_Sim_WidgetImpl import EqualSimWidgetImpl
from Equal_Calc_Widget_Impl import EqualWidgetImpl
from Single_Calc_Widget_Impl import SingleCalcWidgetImpl
from Single_Sim_Widget_Impl import SingleSimWidgetImpl
from TransWidgetImpl import TransWidgetImpl


class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        self.setStyleSheet('''
                            QWidget {
                                background-color: white;
                                border: none;
                                border-bottom-right-radius:10px solid #cccccc;
                                border-top-right-radius:10px solid #cccccc;
                            }
                        ''')

        mainVLay = QVBoxLayout()
        self.stackedWidget = QStackedWidget()

        # 创建页面
        # self.page0 = QWidget()

        # 同步摆计算界面
        self.wEqual = QMainWindow()
        self.wEqualWidgetImpl = EqualWidgetImpl(self.wEqual)

        # 同步摆仿真界面
        self.wEqualSim = QMainWindow()
        self.wEqualSimWidgetImpl = EqualSimWidgetImpl(self.wEqualSim)

        # 双头摆计算界面
        self.wDoubleCalc = QMainWindow()
        self.wDoubleCalcWidgetImpl = DoubleCalcWidgetImpl(self.wDoubleCalc)
        # 双头摆仿真界面
        self.wDoubleSim = QMainWindow()
        self.wDoubleSimWidgetImpl = DoubleSimWidgetImpl(self.wDoubleSim)
        # 单头摆计算界面
        self.wSingleCalc = QMainWindow()
        self.wSingleCalcWidgetImpl = SingleCalcWidgetImpl(self.wSingleCalc)
        # 单头摆仿真界面
        self.wSingleSim = QMainWindow()
        self.wSingleSimWidgetImpl = SingleSimWidgetImpl(self.wSingleSim)

        # self.wTrans = QWidget()
        # self.wTransWidgetImpl = TransWidgetImpl(self.wTrans)


        # 添加页面到QStackedWidget
        self.stackedWidget.addWidget(self.wEqual)
        self.stackedWidget.addWidget(self.wEqualSim)
        self.stackedWidget.addWidget(self.wDoubleCalc)
        self.stackedWidget.addWidget(self.wDoubleSim)
        self.stackedWidget.addWidget(self.wSingleCalc)
        self.stackedWidget.addWidget(self.wSingleSim)

        mainVLay.addWidget(self.stackedWidget)

        self.setLayout(mainVLay)

        self.gotoPage(0)

    def gotoPage(self, index = 0):
        self.stackedWidget.setCurrentIndex(index)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)