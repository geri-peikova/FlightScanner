"""Tests for Scanned Flight Window"""

# pylint: disable=line-too-long
# pylint: disable=no-name-in-module
import sys
from PyQt5.QtWidgets import QApplication

from flight_scanner.interpreters import get_sorted_list_flights
from flight_scanner.windows import ScannedFlightsWindow
from tests.setup import LIST_FLIGHTS_UNSORTED, INPUT_DATA


def scanned_flights_window():
    """
    Test Scanned Flight Window with fake data
    """
    app = QApplication(sys.argv)
    window = ScannedFlightsWindow(get_sorted_list_flights(LIST_FLIGHTS_UNSORTED), INPUT_DATA)
    window.show()
    sys.exit(app.exec_())
