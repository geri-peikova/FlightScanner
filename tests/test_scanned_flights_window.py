import sys
from PyQt5.QtWidgets import QApplication

from interpreters import get_sorted_list_flights
from windows import ScannedFlightsWindow
from tests.setup import LIST_FLIGHTS_UNSORTED, INPUT_DATA


def scanned_flights_window():
    app = QApplication(sys.argv)
    window = ScannedFlightsWindow(get_sorted_list_flights(LIST_FLIGHTS_UNSORTED), INPUT_DATA)
    window.show()
    sys.exit(app.exec_())
