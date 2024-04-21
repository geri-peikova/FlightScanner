import sys

from PyQt5.QtWidgets import QApplication

from windows import ScannedFlightsWindow
from flight_scanner import get_sorted_list_flights
from tests.setup import LIST_FLIGHTS_UNSORTED, INPUT_DATA


def test_scanned_flights_window():
    app = QApplication(sys.argv)
    window = ScannedFlightsWindow(get_sorted_list_flights(LIST_FLIGHTS_UNSORTED), INPUT_DATA)
    window.show()
    sys.exit(app.exec_())
