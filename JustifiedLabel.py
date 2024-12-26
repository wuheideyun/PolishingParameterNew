import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout
from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtCore import Qt

class JustifiedLabel(QLabel):
    def __init__(self, text,fixed_width = 0, parent=None):
        super().__init__(text, parent)
        self.fixed_width = fixed_width
        self.setTextFormat(Qt.PlainText)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        metrics = QFontMetrics(self.font())
        text = self.text()
        width = self.width()
        height = self.height()

        # 分离冒号
        if '：' in text:
            text_before_colon, colon = text.split('：')
            colon = '：'
        else:
            text_before_colon = text
            colon = ''

        # colon = '：'

        # 计算每个字符的宽度
        char_widths = [metrics.horizontalAdvance(char) for char in text_before_colon]
        if self.fixed_width != 0:
            total_width = self.fixed_width
        else:
            total_width = sum(char_widths)

        # 计算每个字符的间距
        spacing = (width - total_width - metrics.horizontalAdvance(colon)) / (len(text_before_colon) - 1) if len(text_before_colon) > 1 else 0

        x = 0
        for i, char in enumerate(text_before_colon):
            char_width = char_widths[i]
            painter.drawText(x, 0, char_width, height, Qt.AlignLeft | Qt.AlignVCenter, char)
            x += char_width + spacing

        # 绘制冒号
        if colon:
            colon_width = metrics.horizontalAdvance(colon)
            painter.drawText(width - colon_width, 0, colon_width, height, Qt.AlignRight | Qt.AlignVCenter, colon)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("整齐排列的QLabel和编辑框")
        self.setGeometry(100, 100, 400, 300)

        # 创建网格布局
        layout = QGridLayout()

        # 定义标签和编辑框的文本
        labels = [
            "主皮带速度(mm/s)：", "摆动速度(mm/s)：", "匀速摆动时间(s)：", "边部停留时间(s)：",
            "摆     幅(mm)：", "同粒度磨头数(个)：", "均匀系数："
        ]

        # 定义编辑框的名称
        line_edit_names = [
            "belt_speed", "swing_speed", "uniform_swing_time", "edge_stay_time",
            "swing_amplitude", "grit_head_count", "uniform_coefficient"
        ]

        # 创建编辑框的集合
        self.line_edits = []

        # 将标签和编辑框添加到网格布局中
        for row, (label_text, line_edit_name) in enumerate(zip(labels, line_edit_names)):
            label = JustifiedLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setFixedWidth(7)
            line_edit.setObjectName(line_edit_name)  # 设置编辑框的名称
            self.line_edits.append(line_edit)  # 将编辑框添加到集合中
            layout.addWidget(label, row, 0)  # 标签放在第0列
            layout.addWidget(line_edit, row, 1)  # 编辑框放在第1列

        # 设置窗口的布局
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())