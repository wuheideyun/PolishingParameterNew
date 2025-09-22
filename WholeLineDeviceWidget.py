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
        self.head_count_edit.setFixedWidth(50)

        between_label = QLabel("磨头间距(mm):", self)
        between_label.setFont(font)
        self.between_edit = QLineEdit(self)
        self.between_edit.setFont(font)
        self.between_edit.setStyleSheet("color: black; padding: 2px;")
        double_validator = QDoubleValidator()
        double_validator.setDecimals(2)
        self.between_edit.setValidator(double_validator)
        self.between_edit.setFixedWidth(50)



        beam_between_label = QLabel("横梁间距(mm):", self)
        beam_between_label.setFont(font)
        self.beam_between_edit = QLineEdit(self)
        self.beam_between_edit.setFont(font)
        self.beam_between_edit.setStyleSheet("color: black; padding: 2px;")
        self.beam_between_edit.setValidator(QDoubleValidator(0, 99999, 2, self))
        self.beam_between_edit.setFixedWidth(50)

        ceramic_width_label = QLabel("进砖宽度(mm):", self)
        ceramic_width_label.setFont(font)
        self.ceramic_width_edit = QLineEdit(self)
        self.ceramic_width_edit.setFont(font)
        self.ceramic_width_edit.setStyleSheet("color: black; padding: 2px;")
        self.ceramic_width_edit.setValidator(QDoubleValidator(0, 99999, 2, self))
        self.ceramic_width_edit.setFixedWidth(50)

        belt_speed_label = QLabel("主皮带速度(mm/s):", self)
        belt_speed_label.setFont(font)
        self.belt_speed_edit = QLineEdit(self)
        self.belt_speed_edit.setFont(font)
        self.belt_speed_edit.setStyleSheet("color: black; padding: 2px;")
        self.belt_speed_edit.setValidator(QDoubleValidator(0, 99999, 2, self))
        self.belt_speed_edit.setFixedWidth(50)

        beam_swing_tempo_label = QLabel("横梁摆动快慢:", self)
        beam_swing_tempo_label.setFont(font)
        self.beam_swing_tempo_combo = QComboBox(self)
        self.beam_swing_tempo_combo.setFont(font)
        self.beam_swing_tempo_combo.setStyleSheet("color: black; padding: 2px;")
        self.beam_swing_tempo_combo.setFixedWidth(64)
        self.beam_swing_tempo_combo.addItem("慢速", 0)
        self.beam_swing_tempo_combo.addItem("快速", 1)

        conversion_label = QLabel("换算:", self)
        conversion_label.setFont(font)
        self.conversion_combo = QComboBox(self)
        self.conversion_combo.setFont(font)
        self.conversion_combo.setStyleSheet("color: black; padding: 2px;")
        self.conversion_combo.setFixedWidth(90)
        main_layout.addWidget(type_label)
        main_layout.addWidget(self.type_combo)
        main_layout.addWidget(head_count_label)
        main_layout.addWidget(self.head_count_edit)
        main_layout.addWidget(between_label)
        main_layout.addWidget(self.between_edit)
        main_layout.addWidget(beam_between_label)
        main_layout.addWidget(self.beam_between_edit)
        main_layout.addWidget(ceramic_width_label)
        main_layout.addWidget(self.ceramic_width_edit)
        main_layout.addWidget(belt_speed_label)
        main_layout.addWidget(self.belt_speed_edit)
        main_layout.addWidget(beam_swing_tempo_label)
        main_layout.addWidget(self.beam_swing_tempo_combo)
        main_layout.addWidget(conversion_label)
        main_layout.addWidget(self.conversion_combo)
        main_layout.addStretch()

        # 信号连接
        if main_dialog and hasattr(main_dialog, 'update_grinding_tab'):
            self.head_count_edit.editingFinished.connect(main_dialog.update_grinding_tab)

    def update_conversion_options(self, options: list):
        """
        新增方法：用于更新换算下拉框的选项，同时尽量保留当前的选择。
        """
        # 记录当前选中的文本
        current_selection = self.conversion_combo.currentText()

        # 更新前先阻塞信号，防止触发不必要的逻辑
        self.conversion_combo.blockSignals(True)
        self.conversion_combo.clear()
        self.conversion_combo.addItems(options)

        # 尝试恢复之前的选择
        index = self.conversion_combo.findText(current_selection)
        if index != -1:
            self.conversion_combo.setCurrentIndex(index)

        # 更新后再解除阻塞
        self.conversion_combo.blockSignals(False)