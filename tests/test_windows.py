"""Tests for loading animation and web scrapping for flights"""

# pylint: disable=no-name-in-module
# pylint: disable=redefined-outer-name

import pytest
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QPushButton

from flight_scanner.windows import MyMenuWindow, ScannedFlightsWindow


@pytest.fixture
def app(qtbot):
    """Fixture to create the application instance."""
    test_app = QApplication([])  # Ensure that there is an instance of QApplication
    qtbot.addWidget(test_app)
    return test_app


@pytest.fixture
def my_menu_window(qtbot):
    """Fixture to create the MyMenuWindow instance."""
    window = MyMenuWindow()
    qtbot.addWidget(window)
    return window


def test_initial_ui_state(my_menu_window):
    """Test the initial state of the UI elements in MyMenuWindow."""
    assert my_menu_window.windowTitle() == 'Flight Scanner'
    assert isinstance(my_menu_window.departure_weekday_label, QLabel)
    assert isinstance(my_menu_window.week_days_combobox1, QComboBox)
    assert isinstance(my_menu_window.arrival_weekday_label, QLabel)
    assert isinstance(my_menu_window.week_days_combobox2, QComboBox)
    assert isinstance(my_menu_window.from_textbox, QLineEdit)
    assert my_menu_window.from_textbox.text() == 'Sofia'
    assert isinstance(my_menu_window.to_textbox, QLineEdit)
    assert my_menu_window.to_textbox.placeholderText() == 'Where to?'
    assert isinstance(my_menu_window.button_look_for_flights, QPushButton)


@pytest.fixture
def scanned_flights_window(qtbot):
    """Fixture to create the ScannedFlightsWindow instance."""
    test_scanned_result = []  # Add sample data as needed
    test_input_data = {'flight_from': 'Sofia', 'flight_to': 'Rome'}
    window = ScannedFlightsWindow(test_scanned_result, test_input_data)
    qtbot.addWidget(window)
    return window


def test_scanned_flights_ui_state(scanned_flights_window):
    """Test the initial state of the UI elements in ScannedFlightsWindow."""
    assert scanned_flights_window.windowTitle() == 'Cheapest flights List'
    assert isinstance(scanned_flights_window.label_round_trip, QLabel)
    assert scanned_flights_window.label_round_trip.text() == "Round trip: Sofia - Rome"
