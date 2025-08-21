from PySide6.QtWidgets import (
    QWidget, QGroupBox, QHBoxLayout, QLabel, QComboBox, QLineEdit
)
from PySide6.QtGui import QFont, QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt


class WholeLineDeviceWidget(QGroupBox):
    def __init__(self, device_number, main_dialog, parent=None):
        super().__init__(f"{device_number} 号抛光机配置", parent)

        self.setFixedHeight(75)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(8)

        font = QFont("Microsoft YaHei", 11)

        # --- 创建控件 ---
        type_label = QLabel("机型:", self)
        type_label.setFont(font)
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["单头摆", "双头摆", "同步摆"])
        self.type_combo.setFont(font)
        self.type_combo.setStyleSheet("color: black; padding: 2px;")

        head_count_label = QLabel("磨头数:", self)
        head_count_label.setFont(font)
        self.head_count_edit = QLineEdit(self)
        self.head_count_edit.setFont(font)
        self.head_count_edit.setStyleSheet("color: black; padding: 2px;")
        self.head_count_edit.setValidator(QIntValidator(0, 100, self))

        between_label = QLabel("磨头间距(mm):", self) # 更新标签文本
        between_label.setFont(font)
        self.between_edit = QLineEdit(self) # 彻底替换变量名
        self.between_edit.setFont(font)
        self.between_edit.setStyleSheet("color: black; padding: 2px;")
        double_validator = QDoubleValidator()
        double_validator.setDecimals(2)
        self.between_edit.setValidator(double_validator)

        beam_between_label = QLabel("横梁间距(mm):", self) # 更新标签文本
        beam_between_label.setFont(font)
        self.beam_between_edit = QLineEdit(self) # 彻底替换变量名
        self.beam_between_edit.setFont(font)
        self.beam_between_edit.setStyleSheet("color: black; padding: 2px;")
        self.beam_between_edit.setValidator(QDoubleValidator(0, 99999, 2, self))

        # --- 添加到布局 ---
        main_layout.addWidget(type_label)
        main_layout.addWidget(self.type_combo)
        main_layout.addWidget(head_count_label)
        main_layout.addWidget(self.head_count_edit)
        main_layout.addWidget(between_label)
        main_layout.addWidget(self.between_edit) # 使用新变量
        main_layout.addWidget(beam_between_label)
        main_layout.addWidget(self.beam_between_edit) # 使用新变量
        main_layout.addStretch()

        # 信号连接
        if main_dialog and hasattr(main_dialog, 'update_grinding_tab'):
            self.head_count_edit.editingFinished.connect(main_dialog.update_grinding_tab)