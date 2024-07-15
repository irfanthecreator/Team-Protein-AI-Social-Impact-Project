# For anaconda installation test
# Delete it later

import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Example')
        self.setGeometry(100, 100, 400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
