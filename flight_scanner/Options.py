from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QFormLayout, QMessageBox

from FlightScanner import scanning


class WeekdaySelector(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weekday Selector")
        self.setGeometry(100, 100, 400, 300)

        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        self.buttons_days_of_week = []
        self.label_from = QLabel('From: ')
        self.textline_from = QLineEdit('Sofia')
        self.textline_from.setToolTip('Airport from which the flight to depart.')
        self.label_to = QLabel('To: ')
        self.textline_to = QLineEdit()
        self.textline_to.setToolTip('Airport to which the flight to arrive.')
        self.button_look_for_flights = QPushButton("Look for flights")

        layout = QFormLayout()
        empty_row = QWidget()
        empty_row.setFixedHeight(20)

        for day in self.days_of_week:
            button = QPushButton(day)
            button.setCheckable(True)
            button.clicked.connect(self.buttons_sequencing)
            self.buttons_days_of_week.append(button)
            layout.addWidget(button)

        layout.addRow(empty_row)
        layout.addRow(self.label_from, self.textline_from)
        layout.addRow(self.label_to, self.textline_to)
        layout.addRow(empty_row)
        layout.addWidget(self.button_look_for_flights)

        self.button_look_for_flights.clicked.connect(self.on_clickable_button_click)
        self.setLayout(layout)

    def on_clickable_button_click(self):
        text_from = self.textline_from.text()
        text_to = self.textline_to.text()

        if (not bool(self.textline_from.text())) or (not bool(self.textline_to.text())):
            info_box(self, 'Information', 'Fill in all details before proceeding!')
        else:
            print("Flight from:", text_from)
            print("Flight to:", text_to)

            print('\nYou will be travelling on: ')
            for day, button in zip(self.days_of_week, self.buttons_days_of_week):
                if button.isChecked():
                    print(' ', day)
        scanning()

    def buttons_sequencing(self):
        sender = self.sender()
        # Whether there is a sequence in checking the buttons
        if sender.isChecked():
            sender.setChecked(False)
            if any(button.isChecked() for button in self.buttons_days_of_week):
                index = self.days_of_week.index(sender.text())
                if (index == 6) and (self.buttons_days_of_week[index - 1].isChecked() or self.buttons_days_of_week[0].isChecked()):
                    sender.setChecked(True)
                elif index == 6 and (not self.buttons_days_of_week[index - 1].isChecked() or not self.buttons_days_of_week[0].isChecked()):
                    sender.setChecked(False)
                    info_box(self, 'Information', 'Days have to be marked in sequence!')
                elif self.buttons_days_of_week[index - 1].isChecked() or self.buttons_days_of_week[index + 1].isChecked():
                    sender.setChecked(True)
                else:
                    sender.setChecked(False)
                    info_box(self, 'Information', 'Days have to be marked in sequence!')
            else:
                sender.setChecked(True)
        # Whether there is a sequence in unchecking the buttons
        if not sender.isChecked():
            sender.setChecked(True)
            if any(not button.isChecked() for button in self.buttons_days_of_week):
                index = self.days_of_week.index(sender.text())
                if (index == 6) and (not self.buttons_days_of_week[index - 1].isChecked() or not self.buttons_days_of_week[0].isChecked()):
                    sender.setChecked(False)
                elif index == 6 and (self.buttons_days_of_week[index - 1].isChecked() or self.buttons_days_of_week[0].isChecked()):
                    sender.setChecked(True)
                    info_box(self, 'Information', 'Days have to be marked in sequence!')
                elif not self.buttons_days_of_week[index - 1].isChecked() or not self.buttons_days_of_week[index + 1].isChecked():
                    sender.setChecked(False)
                else:
                    sender.setChecked(True)
                    info_box(self, 'Information', 'Days have to be marked in sequence!')
            else:
                sender.setChecked(False)


def info_box(self, title, text):
    info_box = QMessageBox()
    info_box.setIcon(QMessageBox.Information)
    info_box.setWindowTitle(title)
    info_box.setText(text)
    info_box.setStandardButtons(QMessageBox.Ok)
    info_box.exec()
