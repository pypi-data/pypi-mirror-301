import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from mango_ui import MangoTabs, MangoPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Tabs Example")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.tab_widget = MangoTabs()

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)
        self.create_tabs()

    def create_tabs(self):
        # 创建第一个选项卡
        tab1 = QWidget()
        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("This is the content of Tab 1"))
        tab1.setLayout(layout1)

        # 创建第二个选项卡
        tab2 = QWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("This is the content of Tab 2"))
        tab2.setLayout(layout2)

        # 创建第三个选项卡
        tab3 = QWidget()
        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel("This is the content of Tab 3"))
        tab3.setLayout(layout3)

        # 添加选项卡到 QTabWidget
        self.tab_widget.addTab(tab1, "Tab 1")
        self.tab_widget.addTab(tab2, "Tab 2")
        self.tab_widget.addTab(tab3, "Tab 3")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
