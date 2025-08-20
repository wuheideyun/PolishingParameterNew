from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QComboBox, QScrollArea
)
from PySide6.QtGui import QFont, QPainter, QColor
from PySide6.QtCore import Qt


# 一个自定义的 Widget，我们手动控制它的背景绘制为深蓝色
class DarkBackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(31, 55, 96))


class WholeLineGrindingHeadWidget(QGroupBox):
    def __init__(self, device_number, head_count, parent=None):
        super().__init__(f"{device_number} 号抛光机磨块配比", parent)

        # --- 新增：初始化用于存储所有下拉框的列表 ---
        self.grit_combos = []

        self.setStyleSheet("""
            GrindingHeadWidget, WholeLineGrindingHeadWidget { /* 增加兼容性 */
                background-color: transparent; 
                font-family: "Microsoft YaHei"; 
                font-size: 14px;
                border: 1px solid #1e5dab; 
                border-radius: 8px; 
                margin-top: 10px;
                padding-top: 20px;
            }
            GrindingHeadWidget::title, WholeLineGrindingHeadWidget::title {
                color: white; 
                subcontrol-origin: margin; 
                subcontrol-position: top center; 
                padding: 0 10px;
            }
            QScrollArea { 
                border: 1px solid #1e5dab; 
                background-color: transparent;
            }
            QLabel { 
                color: white; 
                font-family: "Microsoft YaHei"; 
                font-size: 11px;
                background-color: transparent;
            }
            QComboBox { 
                color: white; 
                background-color: #2c3e50; 
                border: 1px solid #777;
                border-radius: 3px;
                padding: 3px 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
                background-color: #2c3e50;
                border: 1px solid #1e5dab;
                selection-background-color: #1e5dab;
                outline: 0px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = DarkBackgroundWidget()
        scroll_area.setWidget(content_widget)

        grid_layout = QGridLayout(content_widget)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(10)

        grit_options = ["140", "180", "240", "320", "400", "600", "800", "1000", "1200", "2000", "3000", "5000"]

        items_per_row = 4

        for i in range(head_count):
            row = i // items_per_row
            col = i % items_per_row

            head_label = QLabel(f"磨头 #{i + 1}:")
            head_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            grit_combo = QComboBox()
            grit_combo.addItems(grit_options)
            grit_combo.setMinimumWidth(120)

            # --- 新增：将创建的下拉框添加到列表中 ---
            self.grit_combos.append(grit_combo)

            grid_layout.addWidget(head_label, row, col * 2)
            grid_layout.addWidget(grit_combo, row, col * 2 + 1)

        main_layout.addWidget(scroll_area)