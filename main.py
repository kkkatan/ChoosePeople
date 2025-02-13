import sys
import random
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class RandomPicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChoosePeople_v2.1.213 CC 2025 kkkatan.")
        self.setWindowIcon(QIcon("ico2.png"))
        self.setGeometry(100, 200, 100, 200)
        
        # 初始化数据
        self.all_names = []
        self.remaining_names = []
        self.drawn_names = []
        self.image_files = []
        self.is_rolling = False
        self.current_image_index = 0
        
        # 初始化UI
        self.init_ui()
        self.load_data()
        self.load_images()
        
        # 启动时显示默认图片
        self.show_random_image()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        # 左侧图片区域
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedWidth(210)
        self.image_label.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 15px;
            padding: 10px;
        """)
        layout.addWidget(self.image_label)

        # 右侧控制区域
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(30)

       # 添加一个空白区域，使名字往下调
        right_layout.addStretch(1)

        # 显示姓名的标签
        self.name_label = QLabel("GET:200 OK!")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: #6aadff;
                background-color: transparent;
            }
        """)
        right_layout.addWidget(self.name_label)

        # 添加一个空白区域，使按钮和名字之间有空隙
        right_layout.addStretch(1)
        # 按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)


        # 开始按钮
        self.start_btn = QPushButton("开始")
        self.start_btn.setFixedSize(150, 50)
        self.start_btn.clicked.connect(self.toggle_roll)
        self.style_button(self.start_btn, "#6aaddd", "#6aadff")

        # 重置按钮
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setFixedSize(150, 50)
        self.reset_btn.clicked.connect(self.reset)
        self.style_button(self.reset_btn, "#ffadaa", "#ffadca")


        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.reset_btn)
        right_layout.addWidget(button_container)

        layout.addWidget(right_panel)

        # 设置背景渐变
        # self.setStyleSheet(f"""
        #     QMainWindow {{
        #         background: qlineargradient(
        #             x1:0, y1:0, x2:1, y2:1,
        #             stop:0 #6a11cb, stop:1 #2575fc
        #         );
        #     }}
        # """)

    def style_button(self, button, normal_color, hover_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {normal_color};
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                padding: 8px 18px;
            }}
        """)
        # 添加动画效果
        self.add_button_animation(button)

    def add_button_animation(self, button):
        # 悬停动画
        hover_anim = QPropertyAnimation(button, b"geometry")
        hover_anim.setDuration(100)
        hover_anim.setEasingCurve(QEasingCurve.OutQuad)

        # 点击动画
        press_anim = QPropertyAnimation(button, b"geometry")
        press_anim.setDuration(100)
        press_anim.setEasingCurve(QEasingCurve.OutQuad)

        # 安装事件过滤器
        button.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.animate_button(obj, 5)
        elif event.type() == QEvent.Leave:
            self.animate_button(obj, -5)
        return super().eventFilter(obj, event)

    def animate_button(self, button, offset):
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.OutBack)
        new_rect = button.geometry().adjusted(-offset, -offset, offset, offset)
        anim.setEndValue(new_rect)
        anim.start()

    def load_data(self):
        try:
            with open("names.txt", "r", encoding="utf-8") as f:
                self.all_names = [line.strip() for line in f if line.strip()]
            self.remaining_names = self.all_names.copy()
        except FileNotFoundError:
            QMessageBox.critical(self, "ERROR", "找不到names.txt文件！")
            sys.exit(1)

    def load_images(self):
        img_dir = Path("images")
        if img_dir.exists():
            self.image_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
        else:
            QMessageBox.warning(self, "WARNING", "找不到图片目录！")

    def show_random_image(self):
        if self.image_files:
            img_path = random.choice(self.image_files)
            pixmap = QPixmap(str(img_path))
            # 修改这里的尺寸为 200x200
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)

    def toggle_roll(self):
        if not self.remaining_names:
            QMessageBox.warning(self, "提示", "所有名字都已抽完！")
            return

        self.is_rolling = not self.is_rolling
        if self.is_rolling:
            self.start_btn.setText("就你了")
            self.start_roll()
        else:
            self.stop_roll()

    def start_roll(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_name)
        self.timer.start(50)

    def update_name(self):
        if self.remaining_names:
            name = random.choice(self.remaining_names)
            self.name_label.setText(name)
            # 添加缩放动画
            self.animate_label()

    def animate_label(self):
        anim = QPropertyAnimation(self.name_label, b"geometry")
        anim.setDuration(100)
        anim.setEasingCurve(QEasingCurve.OutBack)
        original = self.name_label.geometry()
        anim.setKeyValueAt(0.5, original.adjusted(-10, -10, 10, 10))
        anim.setEndValue(original)
        anim.start()

    def stop_roll(self):
        self.timer.stop()
        selected = self.name_label.text()
        if selected in self.remaining_names:
            self.remaining_names.remove(selected)
            self.drawn_names.append(selected)
        self.show_random_image()
        self.start_btn.setText("START")
        self.is_rolling = False

        # 显示结果动画
        self.show_result_animation(selected)

    def show_result_animation(self, name):
        anim = QPropertyAnimation(self.name_label, b"scale")
        anim.setDuration(1000)
        anim.setKeyValueAt(0, 1)
        anim.setKeyValueAt(0.3, 1.2)
        anim.setKeyValueAt(1, 1)
        anim.start()

    def reset(self):
        self.remaining_names = self.all_names.copy()
        self.drawn_names = []
        self.name_label.setText("已重置")
        self.show_random_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = RandomPicker()
    window.show()
    sys.exit(app.exec())
