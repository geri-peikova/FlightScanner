import threading
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QLineEdit, QVBoxLayout, QPushButton,
                             QMessageBox, QGridLayout, QFrame)
from PyQt5 import QtCore, QtGui

from date_utils import format_datetime_to_textdate_and_time, get_travel_dates
from interpreters import open_link, get_sorted_list_flights
from threads import LoadingThread, ScanningThread


class MyMenuWindow(QWidget):
    """
    A window that allows users to select departure and arrival days,
    and search for flights.
    """
    def __init__(self):
        """
        Initializes the MyMenuWindow.
        """
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Sets up the user interface elements of the window.
        """
        font_size = 30  # 14 TODO: Change to 14 for the laptop scale
        self.setFixedSize(1920, 1080)
        self.setWindowTitle('Flight Scanner')
        self.setWindowIcon(QtGui.QIcon('flight_scanner_logo.png'))
        self.setStyleSheet('background: #e9f6fc')

        # Create UI components
        self.departure_weekday_label = QLabel('Select Departure Day:')
        self.departure_weekday_label.setFont(QFont('Arial', font_size))
        self.departure_weekday_label.setStyleSheet('background-color: #bce4f5; padding: 5px; border-radius: 5px;')
        self.week_days_combobox1 = QComboBox(self)
        self.week_days_combobox1.setFont(QFont('Arial', font_size))
        self.week_days_combobox1.addItems(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.week_days_combobox1.setPlaceholderText('Week Days')

        self.arrival_weekday_label = QLabel('Select Arrival Day:')
        self.arrival_weekday_label.setFont(QFont('Arial', font_size))
        self.arrival_weekday_label.setStyleSheet('background-color: #bce4f5; padding: 5px; border-radius: 5px;')
        self.week_days_combobox2 = QComboBox(self)
        self.week_days_combobox2.setFont(QFont('Arial', font_size))
        self.week_days_combobox2.addItems(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.week_days_combobox2.setPlaceholderText('Week Days')

        self.from_label = QLabel('From:')
        self.from_label.setFont(QFont('Arial', font_size))
        self.from_label.setAlignment(QtCore.Qt.AlignRight)
        self.from_label.setStyleSheet('background-color: #bce4f5; padding: 5px; border-radius: 5px;')
        self.from_textbox = QLineEdit('Sofia', self)
        self.from_textbox.setFont(QFont('Arial', font_size))
        self.from_textbox.setPlaceholderText('From where?')
        self.from_textbox.setStyleSheet('background-color: #bce4f5; border: 1px solid #29AAE1; padding: 5px; border-radius: 5px;')

        self.to_label = QLabel('To:')
        self.to_label.setFont(QFont('Arial', font_size))
        self.to_label.setAlignment(QtCore.Qt.AlignRight)
        self.to_label.setStyleSheet('background-color: #bce4f5; padding: 5px; border-radius: 5px;')
        self.to_textbox = QLineEdit(self)
        self.to_textbox.setFont(QFont('Arial', font_size))
        self.to_textbox.setPlaceholderText('Where to?')
        self.to_textbox.setStyleSheet('background-color: #bce4f5; border: 1px solid #29AAE1; padding: 5px; border-radius: 5px;')

        self.button_look_for_flights = QPushButton("Look for flights")
        self.button_look_for_flights.setFont(QFont('Arial', font_size))
        self.button_look_for_flights.setStyleSheet(
            '''
            QPushButton {
                background-color: #29AAE1;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
            }
            QPushButton:hover {
                background-color: #1d95c9;
            }
            '''
        )

        self.label_loading = QLabel('')
        self.label_loading.setFont(QFont('Arial', font_size * 2))
        self.label_loading.setAlignment(QtCore.Qt.AlignCenter)

        self.loading_thread = None

        main_layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout2 = QGridLayout()

        layout1.addWidget(self.departure_weekday_label, 0, 1)
        layout1.addWidget(self.week_days_combobox1, 0, 2)
        layout1.addWidget(self.arrival_weekday_label, 0, 3)
        layout1.addWidget(self.week_days_combobox2, 0, 4)

        layout1.addWidget(self.from_label, 1, 1)
        layout1.addWidget(self.from_textbox, 1, 2)
        layout1.addWidget(self.to_label, 1, 3)
        layout1.addWidget(self.to_textbox, 1, 4)

        layout2.addWidget(self.button_look_for_flights, 0, 1)
        layout2.addWidget(self.label_loading, 1, 1)

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)

        self.button_look_for_flights.clicked.connect(self.on_click_look_for_flights_button)

        self.setLayout(main_layout)
        self.show()

    def on_click_look_for_flights_button(self):
        """
        Handles the click event for the 'Look for flights' button.
        """
        list_flights = []
        input_data = {
            'departure_weekday': self.week_days_combobox1.currentText(),
            'arrival_weekday': self.week_days_combobox2.currentText()
        }

        if not self.from_textbox.text() or not self.to_textbox.text():
            popup_info_box('Information', 'Fill in all details before proceeding!')
        else:
            input_data['flight_from'] = self.from_textbox.text()
            input_data['flight_to'] = self.to_textbox.text()
            print('\nFlight data: ', input_data)
            input_data['dates_list'] = get_travel_dates(
                self.week_days_combobox1.currentText(),
                self.week_days_combobox2.currentText()
            )
            print(input_data['dates_list'])

            self.loading_thread = LoadingThread(self, self.label_loading)
            self.loading_thread.start()

            threads = []
            for index, travel_dates in enumerate(input_data['dates_list']):
                lock = threading.Lock()
                scanning_thread = ScanningThread(self, index, input_data, list_flights, lock)
                threads.append(scanning_thread)
                scanning_thread.start()

            for thread in threads:
                thread.join()

            self.loading_thread.stop()

            if len(list_flights) < 1:
                popup_info_box('Warning', 'The submitted information is incorrect. Fill in the correct data.')
            else:
                print('Sorting flights by price.')
                list_flights = get_sorted_list_flights(list_flights)
                self.scanned_flight_window = ScannedFlightsWindow(list_flights, input_data)
                self.scanned_flight_window.show()
                self.hide()


class ScannedFlightsWindow(QWidget):
    """
    A window that displays the scanned flights results.
    """
    def __init__(self, scanned_result, input_data):
        """
        Initializes the ScannedFlightsWindow with scanned results and input data.
        """
        super().__init__()
        self.init_ui(scanned_result, input_data)

    def init_ui(self, scanned_result, input_data):
        """
        Sets up the user interface elements to display scanned flight data.

        Parameters
        ----------
        scanned_result : list
            The list of scanned flights.
        input_data : dict
            The input data containing flight details.
        """
        font_size = 14  # 4 TODO: Change to 4 for the laptop scale
        self.setFixedSize(1920, 1080)
        self.setWindowTitle('Cheapest flights List')
        self.setWindowIcon(QtGui.QIcon('flight_scanner_logo.png'))
        self.setStyleSheet('background: #e9f6fc')

        self.label_round_trip = QLabel(f"Round trip: {input_data['flight_from']} - {input_data['flight_to']}")
        self.label_round_trip.setFont(QFont('Brush Script MT', font_size * 2))
        self.label_round_trip.setAlignment(QtCore.Qt.AlignCenter)
        self.label_round_trip.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.label_round_trip.setStyleSheet("QFrame { border-radius: 10px; border: 2px solid #29AAE1; }")

        main_layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout2 = QGridLayout()

        buttons = []
        for i, flight in enumerate(scanned_result):
            label_price = QLabel(f"{i + 1} | Price: {flight.price} |")
            label_price.setFont(QFont('Brush Script MT', font_size * 2))
            label_price.setStyleSheet('background-color: #bce4f5; border: 1px solid #29AAE1; padding: 5px; border-radius: 5px;')
            layout2.addWidget(label_price, i + 1, 0)

            label_departure = QLabel(f"| Departure: {format_datetime_to_textdate_and_time(flight.departure_flight.departure_time)} |")
            label_departure.setFont(QFont('Brush Script MT', font_size * 2))
            label_departure.setStyleSheet('background-color: #bce4f5; border: 1px solid #29AAE1; padding: 5px; border-radius: 5px;')
            layout2.addWidget(label_departure, i + 1, 1)

            label_return = QLabel(f"| Return: {format_datetime_to_textdate_and_time(flight.arrival_flight.arrival_time)} |")
            label_return.setFont(QFont('Brush Script MT', font_size * 2))
            label_return.setStyleSheet('background-color: #bce4f5; border: 1px solid #29AAE1; padding: 5px; border-radius: 5px;')
            layout2.addWidget(label_return, i + 1, 2)

            button = QPushButton("More Data")
            button.setFont(QFont('Brush Script MT', font_size * 2))
            button.setStyleSheet(
                '''
                QPushButton {
                    background-color: #29AAE1;
                    color: white;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: transparent;
                    padding: 6px;
                    box-shadow: 10px 10px 10px grey;
                }
                QPushButton:hover {
                    background-color: #1d95c9;
                }
                QPushButton:pressed {
                    background-color: #2c3e50;
                }
                '''
            )
            layout2.addWidget(button, i + 1, 3)
            buttons.append(button)
            button.clicked.connect(lambda checked, url=flight.link: open_link(url))

        layout1.addWidget(QWidget(), 1, 1)
        layout1.addWidget(self.label_round_trip, 2, 2)
        layout1.addWidget(QWidget(), 3, 3)

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)

        self.setLayout(main_layout)
        self.show()


def popup_info_box(title, text):
    """
    Displays an information popup box.

    Parameters
    ----------
    title : str
        The title of the popup window.
    text : str
        The message text to display in the popup window.
    """
    info_box = QMessageBox()
    info_box.setIcon(QMessageBox.Information)
    info_box.setWindowTitle(title)
    info_box.setText(text)
    info_box.setStandardButtons(QMessageBox.Ok)
    info_box.exec()
