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
        # 新增：添加整数校验器
        self.head_count_edit.setValidator(QIntValidator(0, 100, self)) # 允许0-100的整数

        head_spacing_label = QLabel("磨头间距(mm):", self)
        head_spacing_label.setFont(font)
        self.head_spacing_edit = QLineEdit(self)
        self.head_spacing_edit.setFont(font)
        self.head_spacing_edit.setStyleSheet("color: black; padding: 2px;")
        # 新增：添加浮点数校验器
        double_validator = QDoubleValidator()
        double_validator.setDecimals(2) # 允许两位小数
        self.head_spacing_edit.setValidator(double_validator)

        beam_spacing_label = QLabel("横梁间距(mm):", self)
        beam_spacing_label.setFont(font)
        self.beam_spacing_edit = QLineEdit(self)
        self.beam_spacing_edit.setFont(font)
        self.beam_spacing_edit.setStyleSheet("color: black; padding: 2px;")
        # 新增：为横梁间距也添加浮点数校验器
        self.beam_spacing_edit.setValidator(QDoubleValidator(0, 99999, 2, self))


        # --- 添加到布局 ---
        main_layout.addWidget(type_label)
        main_layout.addWidget(self.type_combo)
        main_layout.addWidget(head_count_label)
        main_layout.addWidget(self.head_count_edit)
        main_layout.addWidget(head_spacing_label)
        main_layout.addWidget(self.head_spacing_edit)
        main_layout.addWidget(beam_spacing_label)
        main_layout.addWidget(self.beam_spacing_edit)
        main_layout.addStretch()

        # 信号连接
        if main_dialog and hasattr(main_dialog, 'update_grinding_tab'):
            self.head_count_edit.editingFinished.connect(main_dialog.update_grinding_tab)