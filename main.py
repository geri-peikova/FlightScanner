import sys
from PyQt5.QtWidgets import QApplication

from FlightScanner import scanning
from Options import WeekdaySelector
from dummyD import MyWidget

if __name__ == '__main__':
    """
    app = QApplication(sys.argv)
    window = WeekdaySelector()
    window.show()
    sys.exit(app.exec_())"""

    app = QApplication(sys.argv)
    window = MyWidget()
    sys.exit(app.exec_())
    #scanning()
