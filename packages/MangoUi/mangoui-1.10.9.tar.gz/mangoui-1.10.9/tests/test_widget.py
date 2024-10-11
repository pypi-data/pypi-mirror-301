import random

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel

from mango_ui import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MangoToggle Test")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        self.label = QLabel("Toggle State: OFF")
        layout.addWidget(self.label)

        self.toggle = MangoToggle()
        self.toggle.click.connect(self.update_label)
        self.toggle.set_value(True)
        layout.addWidget(self.toggle)

        self.input = MangoLineEdit('请输入')
        layout.addWidget(self.input)
        self.setLayout(layout)

    def update_label(self, state):
        self.toggle.set_value(False)
        success = random.choice([True, False])  # 模拟请求成功或失败
        # self.toggle.change_requested.emit(success)  # 连接请求信号

        if success:
            self.label.setText("Toggle State: ON")
        else:
            self.label.setText("Toggle State: OFF")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
