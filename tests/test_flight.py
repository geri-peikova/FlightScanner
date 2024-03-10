import pytest
from Flight import get_departure, get_arrival

FLIGHT_INFO_1 = {
    'price': 'BGN 176',
    'departure_flight': 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions',
    'arrival_flight': 'Tue, Sep 3\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions',
    'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'
    }

FLIGHT_INFO_2 = {
            'price': 'BGN 409',
            'departure_flight': 'Mon, Sep 2\n9:50\u202fPM\n – \n10:50\u202fPM\nWizz Air\n2 hr\nSOF–FCO\nNonstop\n84 kg CO2e\n-8% emissions',
            'arrival_flight': 'Tue, Sep 3\n10:50\u202fAM\n – \n6:45\u202fPM\nLufthansa\n6 hr 55 min\nFCO–SOF\n1 stop\n3 hr 30 min MUC\n188 kg CO2e\n+107% emissions',
            'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoyMDI0LT'
    }

FLIGHT_INFO_3 = {
    'price': 'BGN 590',
    'departure_flight': 'Mon, Sep 2\n6:40\u202fPM\n – \n9:25\u202fAM+1\nLOT\n15 hr 45 min\nSOF–FCO\n1 stop\n11 hr 40 min WAW\n244 kg CO2e\n+168% emissions',
    'arrival_flight': 'Tue, Sep 3\n7:40\u202fPM\n – \n1:55\u202fPM+1\nLOT\n17 hr 15 min\nFCO–SOF\n1 stop\n12 hr 50 min WAW\n244 kg CO2e\n+168% emissions',
    'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpqEg'
    }


INPUT_DATA = {
    'departure_weekday': 'Friday',
    'arrival_weekday': 'Sunday',
    'flight_from': 'Sofia',
    'flight_to': 'Rome',
    'dates_list': [{'End': 'Tue, Sep 3', 'Start': 'Mon, Sep 2'},
                   {'End': 'Tue, Sep 10', 'Start': 'Mon, Sep 9'},
                   {'End': 'Tue, Sep 17', 'Start': 'Mon, Sep 16'}]}


def test_get_departure():
    result = get_departure(FLIGHT_INFO_1['departure_flight'], INPUT_DATA)
    assert result == 'Sofia, SOF'


def test_get_arrival():
    result = get_arrival(FLIGHT_INFO_1['arrival_flight'], INPUT_DATA)
    assert result == 'Rome, CIA'
