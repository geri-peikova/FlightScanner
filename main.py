import sys
from PyQt5.QtWidgets import QApplication

from flight_scanner import scanning
from MyMenuWindow import MyMenuWindow

if __name__ == '__main__':
    """
    app = QApplication(sys.argv)
    window = WeekdaySelector()
    window.show()
    sys.exit(app.exec_())"""

    app = QApplication(sys.argv)
    window = MyMenuWindow()
    window.show()
    sys.exit(app.exec_())

"""
    input_data = {'departure_weekday': 'Friday',
                  'arrival_weekday': 'Sunday',
                  'flight_from': 'Sofia',
                  'flight_to': 'Rome',
                  'dates_list': [{'End': 'Tue, Sep 3', 'Start': 'Mon, Sep 2'},
                                 {'End': 'Tue, Sep 10', 'Start': 'Mon, Sep 9'},
                                 {'End': 'Tue, Sep 17', 'Start': 'Mon, Sep 16'}]}
    scanning(input_data)
    """