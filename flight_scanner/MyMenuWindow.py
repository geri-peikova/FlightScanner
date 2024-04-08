from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QMessageBox, QGridLayout, QApplication
from PyQt5 import QtCore

from date_utils import format_datetime_to_textdate_and_time, generate_dates
from flight_scanner import scanning
from interpreters import driver_setup
from tests.setup import LIST_FLIGHTS_UNSORTED
from threads import LoadingThread


class MyMenuWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        screen_size = QApplication.primaryScreen().size()
        font_size = int(screen_size.height()/150)
        self.setFixedSize(int(screen_size.width() / 2), int(screen_size.height() / 2))
        self.setWindowTitle('Flight Scanner')
        self.show()

        # Create dropdown menus for days of the week
        self.departure_weekday_label = QLabel('Select Departure Day:')
        self.departure_weekday_label.setFont(QFont('Arial', font_size))
        self.week_days_combobox1 = QComboBox(self)
        self.week_days_combobox1.setFont(QFont('Arial', font_size))
        self.week_days_combobox1.addItems(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.week_days_combobox1.setPlaceholderText('Week Days')

        self.arrival_weekday_label = QLabel('Select Arrival Day:')
        self.arrival_weekday_label.setFont(QFont('Arial', font_size))
        self.week_days_combobox2 = QComboBox(self)
        self.week_days_combobox2.setFont(QFont('Arial', font_size))
        self.week_days_combobox2.addItems(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.week_days_combobox2.setPlaceholderText('Week Days')

        # Create textboxes with default and hint text
        self.from_label = QLabel('From:')
        self.from_label.setFont(QFont('Arial', font_size))
        self.from_textbox = QLineEdit('Sofia', self)
        self.from_textbox.setFont(QFont('Arial', font_size))
        self.from_textbox.setPlaceholderText('From where?')

        self.to_label = QLabel('To:')
        self.to_label.setFont(QFont('Arial', font_size))
        self.to_textbox = QLineEdit(self)
        self.to_textbox.setFont(QFont('Arial', font_size))
        self.to_textbox.setPlaceholderText('Where to?')

        self.button_look_for_flights = QPushButton("Look for flights")
        self.button_look_for_flights.setFont(QFont('Arial', font_size))

        self.label_loading = QLabel('')
        self.label_loading.setFont(QFont('Arial', font_size*2))
        self.label_loading.setAlignment(QtCore.Qt.AlignCenter)

        self.loading_thread = None

        # Set up layout
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QGridLayout()

        layout1.addWidget(self.departure_weekday_label)
        layout1.addWidget(self.week_days_combobox1)
        layout1.addWidget(self.arrival_weekday_label)
        layout1.addWidget(self.week_days_combobox2)

        layout2.addWidget(self.from_label)
        layout2.addWidget(self.from_textbox)
        layout2.addWidget(self.to_label)
        layout2.addWidget(self.to_textbox)

        layout3.addWidget(self.button_look_for_flights, 0, 1)
        layout3.addWidget(self.label_loading, 1, 1)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)

        self.button_look_for_flights.clicked.connect(self.on_clickable_button_click)

        self.setLayout(layout)

    def on_clickable_button_click(self):
        input_data = {'departure_weekday': self.week_days_combobox1.currentText(),
                      'arrival_weekday': self.week_days_combobox2.currentText()}

        if (not bool(self.from_textbox.text())) or (not bool(self.to_textbox.text())):
            info_box('Information', 'Fill in all details before proceeding!')

        else:
            input_data['flight_from'] = self.from_textbox.text()
            input_data['flight_to'] = self.to_textbox.text()
            print('\nFlight data: ', input_data)
            input_data['dates_list'] = generate_dates(self.week_days_combobox1.currentText(),
                                                      self.week_days_combobox2.currentText())
            print(input_data['dates_list'])
            self.loading_thread = LoadingThread(self, self.label_loading)
            self.loading_thread.start()
            scanned_result = scanning(input_data)   # TODO: Remove the hashtag
            '''scanned_result = get_sorted_list_flights(
                LIST_FLIGHTS_UNSORTED)  # TODO: this is testing line and you should remove it'''
            self.loading_thread.stop()
            if scanned_result == 1:
                info_box('Warning', 'The submitted information is incorrect. Fill the correct data.')

            self.scanned_flight_window = ScannedFlightsWindow(scanned_result, input_data)
            self.scanned_flight_window.show()
            self.hide()


def info_box(title, text):
    info_box = QMessageBox()
    info_box.setIcon(QMessageBox.Information)
    info_box.setWindowTitle(title)
    info_box.setText(text)
    info_box.setStandardButtons(QMessageBox.Ok)
    info_box.exec()


def open_link(url):
    driver_setup(url)
    # Here you can implement code to open the link in a web browser
    print(f"Opening link: {url}")


class ScannedFlightsWindow(QWidget):
    def __init__(self, scanned_result, input_data):
        super().__init__()

        screen_size = QApplication.primaryScreen().size()
        font_size = int(screen_size.height() / 500)
        self.setFixedSize(int(screen_size.width() / 2), int(screen_size.height() / 2))

        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowTitle('Cheapest flights List')
        self.setStyleSheet('''background: #EBF9FE''')

        self.label_round_trip = QLabel(f"Round trip: {input_data['flight_from']} - {input_data['flight_to']}")
        self.label_round_trip.setFont(QFont('Brush Script MT', font_size * 2))
        layout.addWidget(self.label_round_trip, 0, 0)
        buttons = []
        for i, flight in enumerate(scanned_result):
            label_price = QLabel(f"| Price: {flight.price} |")
            label_price.setFont(QFont('Brush Script MT', font_size * 2))
            label_price.setStyleSheet(
                'background-color: rgba(173, 216, 230, 0.5); border: 1px solid rgba(0, 0, 255, 0.5); padding: 5px; border-radius: 5px;')
            layout.addWidget(label_price, i + 1, 0)
            label_departure = QLabel(
                f"| Departure: {format_datetime_to_textdate_and_time(flight.departure_flight.departure_time)} |")
            label_departure.setFont(QFont('Brush Script MT', font_size * 2))
            label_departure.setStyleSheet(
                'background-color: rgba(173, 216, 230, 0.5); border: 1px solid rgba(0, 0, 255, 0.5); padding: 5px; border-radius: 5px;')
            layout.addWidget(label_departure, i + 1, 1)
            label_return = QLabel(
                f"| Return: {format_datetime_to_textdate_and_time(flight.arrival_flight.arrival_time)} |")
            label_return.setFont(QFont('Brush Script MT', font_size * 2))
            label_return.setStyleSheet(
                'background-color: rgba(173, 216, 230, 0.5); border: 1px solid rgba(0, 0, 255, 0.5); padding: 5px; border-radius: 5px;')
            layout.addWidget(label_return, i + 1, 2)
            button = QPushButton("More Data")
            button.setFont(QFont('Brush Script MT', font_size * 2))
            button.setStyleSheet(
                '''
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: transparent;
                    padding: 6px;
                    box-shadow: 10px 10px 10px grey;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #2c3e50;
                }
                '''
            )
            layout.addWidget(button, i + 1, 3)
            buttons.append(button)
            button.clicked.connect(lambda checked, url=flight.link: open_link(url))
