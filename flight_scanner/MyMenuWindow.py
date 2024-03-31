from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QMessageBox, QListWidget, QListWidgetItem, QGridLayout

from date_utils import format_datetime_to_textdate_and_time
from flight_scanner import scanning, get_sorted_list_flights
from interpreters import driver_setup
from tests.setup import LIST_FLIGHTS_UNSORTED


class MyMenuWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create dropdown menus for days of the week
        departure_weekday_label = QLabel('Select Departure Day:')
        self.week_days_combobox1 = QComboBox(self)
        self.week_days_combobox1.addItems(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.week_days_combobox1.setPlaceholderText('Week Days')

        arrival_weekday_label = QLabel('Select Arrival Day:')
        self.week_days_combobox2 = QComboBox(self)
        self.week_days_combobox2.addItems(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.week_days_combobox2.setPlaceholderText('Week Days')

        # Create textboxes with default and hint text
        from_label = QLabel('From:')
        self.from_textbox = QLineEdit('Sofia', self)
        self.from_textbox.setPlaceholderText('From where?')

        to_label = QLabel('To:')
        self.to_textbox = QLineEdit(self)
        self.to_textbox.setPlaceholderText('Where to?')

        self.button_look_for_flights = QPushButton("Look for flights")

        # Set up layout
        layout = QVBoxLayout()
        day_layout = QHBoxLayout()
        text_layout = QHBoxLayout()

        day_layout.addWidget(departure_weekday_label)
        day_layout.addWidget(self.week_days_combobox1)
        day_layout.addWidget(arrival_weekday_label)
        day_layout.addWidget(self.week_days_combobox2)

        text_layout.addWidget(from_label)
        text_layout.addWidget(self.from_textbox)
        text_layout.addWidget(to_label)
        text_layout.addWidget(self.to_textbox)

        layout.addLayout(day_layout)
        layout.addLayout(text_layout)
        layout.addWidget(self.button_look_for_flights)

        self.button_look_for_flights.clicked.connect(self.on_clickable_button_click)
        self.setLayout(layout)

        self.setGeometry(800, 400, 400, 200)
        self.setWindowTitle('Day and Textbox Selector')
        self.show()

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
            #            scanned_result = scanning(input_data)    TODO: Remove the hashtag
            scanned_result = get_sorted_list_flights(
                LIST_FLIGHTS_UNSORTED)  # TODO: this is testing line and you should remove it
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


def generate_dates(start_day, end_day, num_months=1):
    start_day = get_index_by_weekday_name(start_day)
    end_day = get_index_by_weekday_name(end_day)
    dates_list = []
    today = datetime.now()

    # Find the next Friday
    current_day_of_week = today.weekday()
    days_until_start_day = (start_day - current_day_of_week + 7) % 7
    next_weekday = today + timedelta(days=days_until_start_day)

    # Print all the dates starting from Friday and ending on Monday for the next two months
    while next_weekday + timedelta(days=end_day) <= today + relativedelta(
            months=+num_months):  # Print for the next two months (8 weeks)
        if start_day >= end_day:
            week_set = {
                'End': (next_weekday + timedelta(days=end_day) - timedelta(start_day - 7)).strftime('%a, %b %d')}
        else:
            week_set = {'End': (next_weekday + timedelta(days=end_day)).strftime('%a, %b %d')}
        week_set['Start'] = next_weekday.strftime('%a, %b %d')
        dates_list.append(week_set)
        next_weekday += timedelta(days=7)
    return dates_list


def get_index_by_weekday_name(weekday):
    for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
        if day == weekday:
            return i


def open_link(url):
    driver_setup(url)
    # Here you can implement code to open the link in a web browser
    print(f"Opening link: {url}")


class ScannedFlightsWindow(QWidget):
    def __init__(self, scanned_result, input_data):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)
        self.setGeometry(800, 400, 400, 200)
        self.setWindowTitle('Flights List')

        layout.addWidget(QLabel(f"Round trip: {input_data['flight_from']} - {input_data['flight_to']}"), 0, 0)

        for i, flight in enumerate(scanned_result):
            layout.addWidget(QLabel(f"| Price: {flight.price} |"), i + 1, 0)
            layout.addWidget(QLabel(f"| Departure: {format_datetime_to_textdate_and_time(flight.departure_flight.departure_time)} |"), i + 1, 1)
            layout.addWidget(QLabel(f"| Return: {format_datetime_to_textdate_and_time(flight.arrival_flight.arrival_time)} |"), i + 1, 2)
            button = QPushButton("More Data")
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
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #2c3e50;
                }
                QPushButton:focus {
                    box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
                }
                '''
            )
            layout.addWidget(button, i + 1, 3)
            button.clicked.connect(lambda checked, url=flight.link: open_link(url))


    """
 layout.addWidget(self.flights_list_widget)
 self.flights_list_widget = QListWidget()

 for flight in scanned_result:
     flight_item = QListWidgetItem()
     self.flights_list_widget.addItem(flight_item)
     flight_button = QPushButton(f"Price: {flight.price}, Departure: {flight.departure_flight.departure_time}, Arrival: {flight.arrival_flight.arrival_time}")
     flight_button.clicked.connect(lambda checked, url=flight.link: open_link(url))
     self.flights_list_widget.setItemWidget(flight_item, flight_button)"""
