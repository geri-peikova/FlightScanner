import sys
from PyQt5.QtWidgets import QApplication

from flight_scanner import scanning
from MyMenu import MyMenu

if __name__ == '__main__':
    """
    app = QApplication(sys.argv)
    window = WeekdaySelector()
    window.show()
    sys.exit(app.exec_())

    app = QApplication(sys.argv)
    window = MyMenu()
    sys.exit(app.exec_())"""
    scanning()
