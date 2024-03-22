from datetime import datetime

import pytest
from Flight import get_departure, get_arrival, get_duration, get_departure_time, get_flight_date, convert_date_format, \
    get_arrival_time, Travel, Flight

FLIGHT_INFO_1 = {
    'price': 'BGN 176',
    'departure_flight': 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions',
    'arrival_flight': 'Tue, Sep 3\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions',
    'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'
    }

FLIGHT_INFO_2 = {
            'price': 'BGN 409',
            'departure_flight': 'Mon, Sep 2\n9:50\u202fPM\n – \n10:50\u202fPM\nWizz Air\n45 min\nSOF–FCO\n1h 55 min\n84 kg CO2e\n-8% emissions',
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


def test_travel():
    result = Travel(FLIGHT_INFO_1, INPUT_DATA)
    assert result.link == 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'
    assert result.price == 'BGN 176'
# arrival
    assert result.arrival_flight.arrival == 'Rome, CIA'
    assert result.arrival_flight.arrival_time == datetime(2024, 9, 3, 13, 20)
    assert result.arrival_flight.company == 'company'
    assert result.arrival_flight.departure == 'Sofia, CIA'
    assert result.arrival_flight.departure_time == datetime(2024, 9, 3, 20, 35)
    assert result.arrival_flight.duration == '1 hr'

# departure
    assert result.arrival_flight.arrival == 'Rome, SOF'
    assert result.arrival_flight.arrival_time == datetime(2024, 9, 2, 14, 10)
    assert result.arrival_flight.company == 'company'
    assert result.arrival_flight.departure == 'Sofia, SOF'
    assert result.arrival_flight.departure_time == datetime(2024, 9, 2, 13, 25)
    assert result.arrival_flight.duration == '1 hr 45 min'


def test_flight():
    result = Flight(FLIGHT_INFO_1['arrival_flight'], INPUT_DATA)
    assert result.arrival == 'Rome, CIA'
    assert result.arrival_time == datetime(2024, 9, 3, 13, 20)
    assert result.company == 'company'
    assert result.departure == 'Sofia, CIA'
    assert result.departure_time == datetime(2024, 9, 3, 20, 35)
    assert result.duration == '1 hr'


def test_get_departure():
    result = get_departure(FLIGHT_INFO_1['departure_flight'], INPUT_DATA)
    assert result == 'Sofia, SOF'


def test_get_arrival():
    result = get_arrival(FLIGHT_INFO_1['arrival_flight'], INPUT_DATA)
    assert result == 'Rome, CIA'


def test_get_duration():
    result = get_duration(FLIGHT_INFO_2['departure_flight'])
    assert result == '45 min'


def test_get_flight_date():
    result = get_flight_date(FLIGHT_INFO_1['departure_flight'])
    assert result == datetime(2024, 9, 2, 0, 0)


def test_convert_date_format():
    result = convert_date_format('Mon, Sep 2')
    assert result == 'Mon, Sep 02'


def test_get_departure_time():
    result = get_departure_time(FLIGHT_INFO_1['departure_flight'])
    assert result == datetime(2024, 9, 2, 13, 25)


def test_get_arrival_time():
    result = get_arrival_time(FLIGHT_INFO_1['departure_flight'])
    assert result == datetime(2024, 9, 2, 14, 10)


""" 
FlightInfo:  {
            'price': 'BGN 176', 
            'departure_flight': 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions', 
            'arrival_flight': 'Tue, Sep 3\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions', 
            'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'
            }

FlightInfo:  {
            'price': 'BGN 409', 
            'departure_flight': 'Mon, Sep 2\n9:50\u202fPM\n – \n10:50\u202fPM\nWizz Air\n2 hr\nSOF–FCO\nNonstop\n84 kg CO2e\n-8% emissions', 
            'arrival_flight': 'Tue, Sep 3\n10:50\u202fAM\n – \n6:45\u202fPM\nLufthansa\n6 hr 55 min\nFCO–SOF\n1 stop\n3 hr 30 min MUC\n188 kg CO2e\n+107% emissions', 
            'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoyMDI0LT'
            }

FlightInfo:  {
            'price': 'BGN 590', 
            'departure_flight': 'Mon, Sep 2\n6:40\u202fPM\n – \n9:25\u202fAM+1\nLOT\n15 hr 45 min\nSOF–FCO\n1 stop\n11 hr 40 min WAW\n244 kg CO2e\n+168% emissions', 
            'arrival_flight': 'Tue, Sep 3\n7:40\u202fPM\n – \n1:55\u202fPM+1\nLOT\n17 hr 15 min\nFCO–SOF\n1 stop\n12 hr 50 min WAW\n244 kg CO2e\n+168% emissions', 
            'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpqEg'
            }

"""