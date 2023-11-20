import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QMessageBox


class MyWidget(QWidget):
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

            print('\nFlight data: %s', input_data)
        # scanning()


def info_box(title, text):
    info_box = QMessageBox()
    info_box.setIcon(QMessageBox.Information)
    info_box.setWindowTitle(title)
    info_box.setText(text)
    info_box.setStandardButtons(QMessageBox.Ok)
    info_box.exec()
