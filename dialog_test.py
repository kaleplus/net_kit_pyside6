import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QSizePolicy
from PySide6.QtCore import QSize

class ConfigWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConfigWindow")
        self.resize(640, 480)
        self.setMaximumSize(QSize(16777215, 480))

        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # 创建 QListWidget
        self.list_widget = QListWidget(self)
        self.main_layout.addWidget(self.list_widget)

        # 添加项目并设置大小
        for i in range(10):
            item = QListWidgetItem(f"Item {i}")
            item.setSizeHint(QSize(200, 50))  # 设置每个项目的大小（宽度200，高度50）
            self.list_widget.addItem(item)

        # 确保 QListWidget 填满可用空间
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec())
