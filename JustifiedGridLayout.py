from functools import partial
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QLineEdit, QLabel
from PySide6.QtCore import Signal

from JustifiedLabel import JustifiedLabel

class JustifiedGridLayout(QGridLayout):
    sig_textChanged = Signal(str, str)  # 定义一个信号，用于通知外部逻辑

    def __init__(self, labels, line_edit_names, verticalSpacing = 6, line_edit_names2=None, rownum=-1, text='', color='', parent=None):
        super().__init__(parent)
        self.labels = labels
        self.line_edit_names = line_edit_names
        self.line_edit_names2 = line_edit_names2 or []
        self.rownum = rownum
        self.text = text
        self.verticalSpacing = verticalSpacing
        self.color = color
        self.max_iterations = len(self.labels)
        self.current_iteration = 0
        self.current_row = 0
        self.line_edits = []
        self.setSpacing(10)  # 设置布局的间距
        self.init_ui()

    def init_ui(self):
        while self.current_row < self.max_iterations:
            label_text, line_edit_name = self.labels[self.current_iteration], self.line_edit_names[self.current_iteration]
            label = JustifiedLabel(label_text)
            # 设置字体大小和字体类型
            param_font = QFont("Microsoft YaHei", 14)  # "Microsoft YaHei" 为字体类型，18 为字体大小
            label.setFont(param_font)
            label.setMinimumSize(150, 30)  # 设置标签的最小大小
            line_edit = QLineEdit()
            line_edit.setObjectName(line_edit_name)  # 设置编辑框的名称
            line_edit.setFont(param_font)
            line_edit.setStyleSheet("color: white")
            line_edit.setMinimumSize(15, 30)  # 设置编辑框的最小大小
            self.line_edits.append(line_edit)  # 将编辑框添加到集合中
            self.addWidget(label, self.current_row, 0)  # 标签放在第0列
            self.addWidget(line_edit, self.current_row, 1)  # 编辑框放在第1列
            self.add_text(self.current_row)
            self.current_iteration += 1
            self.current_row += 1
            self.setVerticalSpacing(self.verticalSpacing)

        # 为需要监听的 QLineEdit 添加 textChanged 信号的监听
        for line_edit_name in self.line_edit_names2:
            for line_edit in self.line_edits:
                if line_edit.objectName() == line_edit_name:
                    # 使用 partial 来绑定当前的 line_edit_name
                    #line_edit.textChanged.connect(partial(self.on_text_changed, line_edit_name))
                    # 修改为 数据输入确定后触发监听
                    line_edit.editingFinished.connect(partial(self.on_text_changed, line_edit_name))

    def add_text(self, row):
        if self.rownum > 0 and self.rownum == row:
            self.current_row += 1
            labeltext = JustifiedLabel(self.text)
            param_font = QFont("Microsoft YaHei", 16)
            labeltext.setFont(param_font)
            # 设置 QLabel 的文本颜色
            labeltext.setStyleSheet(f"color: {self.color};")
            labeltext.setMinimumSize(150, 30)
            self.addWidget(labeltext, self.current_row, 0, 1, 2)
            self.max_iterations += 1

    def get_line_edit_value(self, name):
        """返回指定名称的 QLineEdit 的值"""
        for line_edit in self.line_edits:
            if line_edit.objectName() == name:
                return line_edit.text()
        return None

    def set_line_edit_value(self, name, value):
        """设置指定名称的 QLineEdit 的值"""
        for line_edit in self.line_edits:
            if line_edit.objectName() == name:
                line_edit.setText(value)

    def on_text_changed(self, name):
        """当监听的 QLineEdit 的值发生变化时，触发外部接口"""
        # self.textChanged.emit(name, text)
        value = self.get_line_edit_value(name)
        self.sig_textChanged.emit(name, value)



# 示例使用
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget

    app = QApplication([])

    labels = ["Label 1", "Label 2", "Label 3"]
    line_edit_names = ["edit1", "edit2", "edit3"]
    line_edit_names2 = ["edit1", "edit3"]  # 需要监听的 QLineEdit

    window = QWidget()
    layout = JustifiedGridLayout(labels, line_edit_names,6, line_edit_names2, rownum=1, text="Special Text", color="red")
    window.setLayout(layout)

    # 连接信号到槽函数
    def on_text_changed(name, text):
        print(f"Text changed in {name}: {text}")

    layout.sig_textChanged.connect(on_text_changed)


    window.show()
    app.exec()
