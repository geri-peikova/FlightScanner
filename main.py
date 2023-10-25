import sys
from PyQt5.QtWidgets import QApplication

from FlightScanner import scanning
from Options import WeekdaySelector

if __name__ == '__main__':
    """
    app = QApplication(sys.argv)
    window = WeekdaySelector()
    window.show()
    sys.exit(app.exec_())"""
    scanning()
