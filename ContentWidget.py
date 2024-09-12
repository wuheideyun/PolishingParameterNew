'''

中间内容控件

'''
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QStyleOption, QStyle, QMainWindow, QStatusBar, \
    QSizePolicy

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
            QLineEdit {
                font-size: 13px;
                font-family: "Microsoft YaHei";
                border: none;  
                border-bottom: 1px solid rgb(200, 200, 200);  
                
            }
            QTextEdit {
                border: 1px solid #CAD0EE; 
                border-radius: 2px; /* 轻微的圆角边框 */
            }
            QPushButton {
                background-color: rgb(0, 200, 0); /* 按钮的默认背景色为绿色 */
                color: white; /* 设置按钮文字颜色为白色 */
                border: none; /* 移除边框 */
                padding: 3px; /* 内边距 */
                font-size: 12px; /* 文字大小 */
                border-radius:5px;
            }
            
            QPushButton:hover {
                background-color: #45A049; /* 鼠标悬停时按钮的背景色变深 */
            }
            QPushButton:pressed {
                background-color: #397d3c; /* 鼠标按下时按钮的背景色更深 */
            } 
            
            QCheckBox::indicator:unchecked{ 
                image:url(:CkClose); 
            } 
            QCheckBox::indicator:checked { 
                image: url(:CkOpen); 
            }
            '''
        )

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

        # self.stackedWidget.setVisible(False)

        self.statusBar = QStatusBar()
        self.statusBar.showMessage("欢迎使用，请登录！")
        mainVLay.addWidget(self.statusBar)
        self.setLayout(mainVLay)

        self.gotoPage(0)

    def gotoPage(self, index = 0):
        self.stackedWidget.setCurrentIndex(index)

    def setStackedWidgetVisible(self,flag):
        self.stackedWidget.setVisible(flag)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)