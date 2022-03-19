from PySide6.QtWidgets import QApplication
from main import Main

if __name__ == '__main__':
    app = QApplication()
    # app.setWindowIcon(QIcon("logo.png"))  # 添加图标
    w = Main()
    w.ui.show()
    app.exec()
