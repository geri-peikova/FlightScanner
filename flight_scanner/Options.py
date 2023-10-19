from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QTextEdit, QLabel, QFrame, QFormLayout, \
    QMessageBox


class WeekdaySelector(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weekday Selector")
        self.setGeometry(100, 100, 400, 300)

        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        self.buttons_week_days = []
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
            self.buttons_week_days.append(button)
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
            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Information)
            info_box.setWindowTitle("Information")
            info_box.setText('Fill in all details before proceeding!')
            info_box.setStandardButtons(QMessageBox.Ok)
            info_box.exec()
        else:
            print("Flight from:", text_from)
            print("Flight to:", text_to)

            for day, button in zip(self.days_of_week, self.buttons_week_days):
                if button.isChecked():
                    print(day, "is marked.")


    def show_info_message(self):
        info_box = QMessageBox()
        info_box.setIcon(QMessageBox.Information)
        info_box.setWindowTitle("Information")
        info_box.setText("This is an information message.")
        info_box.setStandardButtons(QMessageBox.Ok)
        info_box.exec()

    def check_sequence(self):
        return True
