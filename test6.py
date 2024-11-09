import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, QListWidget, QListWidgetItem, QFrame, QGridLayout, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("云文件")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f7f9fc;")

        # 主窗口
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # 左侧导航栏
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # 中间内容区域
        content_area = self.create_content_area()
        main_layout.addWidget(content_area)

        # 右侧联系人面板
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel)

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        layout = QVBoxLayout(sidebar)

        # 添加导航栏按钮
        buttons = [("仪表盘", "icons/dashboard.png"), ("文件", "icons/file.png"),
                   ("图片", "icons/image.png"), ("视频、音频", "icons/video.png"),
                   ("其他", "icons/other.png")]

        for text, icon_path in buttons:
            button = QPushButton(text)
            button.setIcon(QIcon(icon_path))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #eef4fc;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 16px;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    background-color: #d4e1ff;
                }
            """)
            layout.addWidget(button)

        return sidebar

    def create_content_area(self):
        content = QWidget()
        content_layout = QVBoxLayout(content)

        # 顶部搜索框和进度条
        search_and_progress = QWidget()
        search_and_progress_layout = QHBoxLayout(search_and_progress)

        search_box = QLineEdit()
        search_box.setPlaceholderText("输入关键词搜索")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
        """)
        search_box.setFixedHeight(40)

        upload_btn = QPushButton("上传文件")
        upload_btn.setIcon(QIcon("icons/upload.png"))
        upload_btn.setFixedHeight(40)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        search_and_progress_layout.addWidget(search_box)
        search_and_progress_layout.addWidget(upload_btn)
        content_layout.addWidget(search_and_progress)

        # 中间卡片区域
        cards_grid = QGridLayout()

        card_data = [
            ("文件", "11 GB", "2023.11.17 11:11", "icons/file_icon.png"),
            ("图片", "21 GB", "2023.11.17 11:11", "icons/image_icon.png"),
            ("视频、音频", "21 GB", "2023.11.17 11:11", "icons/video_icon.png"),
            ("其他", "21 GB", "2023.11.17 11:11", "icons/other_icon.png")
        ]

        for i, (title, size, date, icon_path) in enumerate(card_data):
            card = self.create_info_card(title, size, date, icon_path)
            cards_grid.addWidget(card, i // 2, i % 2)

        content_layout.addLayout(cards_grid)

        return content

    def create_info_card(self, title, size, date, icon_path):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: blue;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #ddd;
            }
        """)
        card_layout = QVBoxLayout(card)

        icon = QLabel()
        icon.setPixmap(QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio))
        icon.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        size_label = QLabel(size)
        size_label.setAlignment(Qt.AlignCenter)
        size_label.setStyleSheet("font-size: 24px; color: #4CAF50;")

        date_label = QLabel(date)
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("font-size: 12px; color: #999;")

        card_layout.addWidget(icon)
        card_layout.addWidget(title_label)
        card_layout.addWidget(size_label)
        card_layout.addWidget(date_label)

        return card

    def create_right_panel(self):
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # 联系人列表
        contact_label = QLabel("联系人")
        contact_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        right_layout.addWidget(contact_label)

        contact_list = QListWidget()
        contacts = ["张宇航 - johndoe1234@gmail.com", "李心怡 - emily.smith567@yahoo.com", "王明阳 - alex.wang@hotmail.com",
                    "赵佳琪 - sarah.jones789@outlook.com", "刘晨辰 - mikebrown12@gmail.com", "郑穆婷 - ohnson456@yahoo.com"]
        for contact in contacts:
            item = QListWidgetItem(contact)
            contact_list.addItem(item)

        right_layout.addWidget(contact_list)

        # 邀请成员区域
        invite_member = QFrame()
        invite_member.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #ddd;
            }
        """)
        invite_layout = QVBoxLayout(invite_member)

        invite_label = QLabel("邀请成员")
        invite_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        invite_code = QLabel("ABSHKHKH51232131")
        invite_code.setStyleSheet("font-size: 16px; color: #4CAF50;")

        copy_btn = QPushButton("复制")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        invite_layout.addWidget(invite_label)
        invite_layout.addWidget(invite_code)
        invite_layout.addWidget(copy_btn)

        right_layout.addWidget(invite_member)

        return right_panel


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
