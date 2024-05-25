import sys
from PyQt5.QtWidgets import QApplication

from flight_scanner.windows import MyMenuWindow

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MyMenuWindow()
    window.show()
    sys.exit(app.exec_())
