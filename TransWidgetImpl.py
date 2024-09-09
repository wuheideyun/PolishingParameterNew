'''

翻译窗口

'''

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

import trans_widget
from test_baidutrans import BaiduTrans


class TransWidgetImpl(QWidget, trans_widget.Ui_Form):
    def __init__(self, w):
        super().__init__()
        self.setupUi(w)

        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_StyledBackground)  # 禁止父窗口样式影响子控件样式

        self.lang_dic = {
            "中文": "zh",
            "英文": "en",
            "韩语": "kor",
            "日语": "jp"
        }

        lang_keys = list(self.lang_dic.keys())
        self.lang_count = len(lang_keys)

        self.comboBox_src.addItems(lang_keys)
        self.comboBox_src.setFixedSize(100, 24)
        self.comboBox_src.setCurrentIndex(1)

        qss = """
            QComboBox {
                /* 设置QComboBox的边框、背景和内边距 */
                border: 1px solid rgb(190, 190, 190);
                background-color: white;
                padding-left: 5px; 
                padding-right: 20px; /* 确保文本不会覆盖箭头 */
                border-bottom-right-radius:0px;
            }
    
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 2px;
                border-left-color: darkgray;
                border-left-style: solid;
                background-color: lightblue; /* 这里设置箭头的背景色 */
            }
    
            QComboBox::down-arrow {
                image: url(:down_arrow); /* 替换为你的图标路径 */
            }
    
            /* 如果你想在下拉时更改样式，可以添加以下部分 */
            QComboBox::down-arrow:on { /* 在QComboBox被按下时 */
                top: 1px;
                left: 1px;
            }
        """

        self.comboBox_src.setStyleSheet(qss)

        self.comboBox_target.addItems(lang_keys)
        self.comboBox_target.setCurrentIndex(0)
        self.comboBox_target.setFixedSize(100, 24)
        self.comboBox_target.setStyleSheet(qss)

        self.comboBox_src.currentIndexChanged.connect(self.OnSrcComboxSelectChanged)
        self.comboBox_target.currentIndexChanged.connect(self.OnTargetComboxSelectChanged)

        self.btnStartTrans.setText("开始翻译")
        self.btnStartTrans.setFixedSize(100, 32)
        self.btnStartTrans.clicked.connect(self.onStartTrans)

        self.btnStartTrans.setStyleSheet("""
           QPushButton {
               background-color: rgb(0, 200, 0); /* 按钮的默认背景色为绿色 */
               color: white; /* 设置按钮文字颜色为白色 */
               border: none; /* 移除边框 */
               padding: 10px; /* 内边距 */
               font-size: 12px; /* 文字大小 */
               border-radius:5px;
           }
           
           QPushButton:hover {
               background-color: #45A049; /* 鼠标悬停时按钮的背景色变深 */
           }
           
           QPushButton:pressed {
               background-color: #397d3c; /* 鼠标按下时按钮的背景色更深 */
           }
       """)

        self.textEdit_src.setStyleSheet("""
            QTextEdit {
                border: 1px solid #CAD0EE; 
                border-radius: 2px; /* 轻微的圆角边框 */
            }
        """)

        self.textEdit_src.setPlaceholderText("请输入或粘贴想要翻译的文本，然后点击开始按钮进行翻译")

        self.textEdit_target.setStyleSheet("""
            QTextEdit {
                border: 1px solid #CAD0EE; 
                border-radius: 2px; /* 轻微的圆角边框 */
            }
        """)

    def onStartTrans(self):
        src = self.textEdit_src.toPlainText()

        baiduTrans = BaiduTrans()

        src_lang_text = self.comboBox_src.currentText()
        target_lang_text = self.comboBox_target.currentText()

        src_lang = self.lang_dic[src_lang_text]
        target_lang = self.lang_dic[target_lang_text]

        transResultJson = baiduTrans.Trans(src, src_lang, target_lang)

        trans_result = transResultJson['trans_result']

        for item in trans_result:
            # print(f"src = {item['src']}, dst = {item['dst']}")
            self.textEdit_target.setText(item['dst'])

    def OnSrcComboxSelectChanged(self, index):
        target_index = self.comboBox_target.currentIndex()

        if index == target_index:
            self.comboBox_target.setCurrentIndex((index + 1) % self.lang_count)

    def OnTargetComboxSelectChanged(self, index):
        src_index = self.comboBox_src.currentIndex()

        if index == src_index:
            self.comboBox_src.setCurrentIndex((index + 1) % self.lang_count)



