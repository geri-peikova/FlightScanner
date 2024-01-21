import sys
from PyQt5.QtWidgets import QApplication

from flight_scanner import scanning
from MyMenu import MyMenu

if __name__ == '__main__':
    """
    app = QApplication(sys.argv)
    window = WeekdaySelector()
    window.show()
    sys.exit(app.exec_())

    app = QApplication(sys.argv)
    window = MyMenu()
    sys.exit(app.exec_())"""

    input_data = {'departure_weekday': 'Friday',
                  'arrival_weekday': 'Sunday',
                  'flight_from': 'Sofia',
                  'flight_to': 'Rome',
                  'dates_list': [{'End': 'Tue, Jan 16', 'Start': 'Mon, Jan 15'},
                                 {'End': 'Tue, Jan 23', 'Start': 'Mon, Jan 22'},
                                 {'End': 'Tue, Jan 30', 'Start': 'Mon, Jan 29'}]}
    scanning(input_data)
