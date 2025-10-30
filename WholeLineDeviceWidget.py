# 文件名: WholeLineDeviceWidget.py (已增加“原点位置”并优化布局)

from PySide6.QtWidgets import (
    QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QComboBox, QLineEdit
)
from PySide6.QtGui import QFont, QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt


class WholeLineDeviceWidget(QGroupBox):
    def __init__(self, device_number, main_dialog, parent=None):
        super().__init__(f"{device_number} 号抛光机配置", parent)

        self.setStyleSheet("QGroupBox { padding-top: 20px; }")

        # --- 主布局使用 QGridLayout ---
        main_layout = QGridLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setHorizontalSpacing(15)  # 列间距
        main_layout.setVerticalSpacing(12)  # 行间距

        font = QFont("Microsoft YaHei", 10)

        # --- 创建所有控件 ---
        type_label = QLabel("机型:", self)
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["单头摆", "双头摆", "同步摆"])

        head_count_label = QLabel("磨头数:", self)
        self.head_count_edit = QLineEdit(self)
        self.head_count_edit.setValidator(QIntValidator(0, 100, self))

        between_label = QLabel("磨头间距(mm):", self)
        self.between_edit = QLineEdit(self)
        self.between_edit.setValidator(QDoubleValidator(0, 99999, 2, self))

        beam_between_label = QLabel("横梁间距(mm):", self)
        self.beam_between_edit = QLineEdit(self)
        self.beam_between_edit.setValidator(QDoubleValidator(0, 99999, 2, self))

        ceramic_width_label = QLabel("进砖宽度(mm):", self)
        self.ceramic_width_edit = QLineEdit(self)
        self.ceramic_width_edit.setValidator(QDoubleValidator(0, 99999, 2, self))

        belt_speed_label = QLabel("主皮带速度(m/s):", self)
        self.belt_speed_edit = QLineEdit(self)
        self.belt_speed_edit.setValidator(QDoubleValidator(0, 99999, 2, self))

        beam_swing_tempo_label = QLabel("横梁摆动快慢:", self)
        self.beam_swing_tempo_combo = QComboBox(self)
        self.beam_swing_tempo_combo.addItems(["慢速", "快速"])

        conversion_label = QLabel("换算:", self)
        self.conversion_combo = QComboBox(self)

        origin_location_label = QLabel("原点位置(mm):", self)
        self.origin_location_edit = QLineEdit(self)
        self.origin_location_edit.setValidator(QDoubleValidator(0, 99999, 2, self))
        all_widgets = self.findChildren(QWidget)
        for widget in all_widgets:
            if isinstance(widget, (QLabel, QLineEdit, QComboBox)):
                widget.setFont(font)
                if isinstance(widget, (QLineEdit, QComboBox)):
                    widget.setStyleSheet("padding: 4px;")

        def create_widget_pair(label, widget):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(label)
            layout.addWidget(widget)
            return container

        type_group = create_widget_pair(type_label, self.type_combo)
        head_count_group = create_widget_pair(head_count_label, self.head_count_edit)
        between_group = create_widget_pair(between_label, self.between_edit)
        beam_between_group = create_widget_pair(beam_between_label, self.beam_between_edit)
        ceramic_width_group = create_widget_pair(ceramic_width_label, self.ceramic_width_edit)
        belt_speed_group = create_widget_pair(belt_speed_label, self.belt_speed_edit)
        beam_swing_tempo_group = create_widget_pair(beam_swing_tempo_label, self.beam_swing_tempo_combo)
        conversion_group = create_widget_pair(conversion_label, self.conversion_combo)
        origin_location_group = create_widget_pair(origin_location_label, self.origin_location_edit)

        # addWidget(widget, row, column, rowSpan, columnSpan)
        # --- 第 0 行 ---
        main_layout.addWidget(type_group, 0, 0, 1, 2)
        main_layout.addWidget(ceramic_width_group, 0, 2, 1, 2)
        main_layout.addWidget(between_group, 0, 4, 1, 2)
        main_layout.addWidget(beam_between_group, 0, 6, 1, 2)
        main_layout.addWidget(origin_location_group, 0, 8, 1, 2)
        # --- 第 1 行 ---
        main_layout.addWidget(beam_swing_tempo_group, 1, 0, 1, 2)
        main_layout.addWidget(belt_speed_group, 1, 2, 1, 2)
        main_layout.addWidget(head_count_group, 1, 4, 1, 2)
        main_layout.addWidget(conversion_group, 1, 6, 1, 2)

        main_layout.setColumnStretch(10, 1) 

        # 信号连接
        if main_dialog and hasattr(main_dialog, 'update_grinding_tab'):
            self.head_count_edit.editingFinished.connect(main_dialog.update_grinding_tab)

    def update_conversion_options(self, options: list):
        current_selection = self.conversion_combo.currentText()
        self.conversion_combo.blockSignals(True)
        self.conversion_combo.clear()
        self.conversion_combo.addItems(options)
        index = self.conversion_combo.findText(current_selection)
        if index != -1:
            self.conversion_combo.setCurrentIndex(index)
        self.conversion_combo.blockSignals(False)