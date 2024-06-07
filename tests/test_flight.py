"""Tests for flight and travel class"""

# pylint: disable=line-too-long

from datetime import datetime
from tests.setup import INPUT_DATA, FLIGHTS_INFO
from flight_scanner.date_utils import convert_date_format
from flight_scanner.flight import get_departure, get_arrival, get_duration, get_departure_time, get_flight_date, \
    get_arrival_time, Travel, Flight


def test_travel():
    """
    Tests the Travel class initialization and attributes.
    """
    result = Travel(FLIGHTS_INFO[0], INPUT_DATA)
    assert result.link == 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'
    assert result.price == 'BGN 176'

    # departure
    assert result.departure_flight.flight_from == 'Sofia, SOF'
    assert result.departure_flight.departure_time == datetime(2024, 9, 2, 13, 25)
    assert result.departure_flight.flight_to == 'Rome, CIA'
    assert result.departure_flight.arrival_time == datetime(2024, 9, 2, 14, 10)
    assert result.departure_flight.company == 'company'
    assert result.departure_flight.duration == '1 hr 45 min'

    # arrival
    assert result.arrival_flight.flight_from == 'Rome, CIA'
    assert result.arrival_flight.departure_time == datetime(2024, 9, 3, 20, 35)
    assert result.arrival_flight.flight_to == 'Sofia, SOF'
    assert result.arrival_flight.arrival_time == datetime(2024, 9, 3, 23, 20)
    assert result.arrival_flight.company == 'company'
    assert result.arrival_flight.duration == '1 hr'


def test_flight():
    """
    Tests the Flight class initialization and attributes.
    """
    result = Flight(FLIGHTS_INFO[0]['departure_flight'], INPUT_DATA, 'straight')
    assert result.flight_from == 'Sofia, SOF'
    assert result.departure_time == datetime(2024, 9, 2, 13, 25)
    assert result.flight_to == 'Rome, CIA'
    assert result.arrival_time == datetime(2024, 9, 2, 14, 10)
    assert result.company == 'company'
    assert result.duration == '1 hr 45 min'


def test_get_departure_straight():
    """
    Tests 'get_departure' for straight flights.
    """
    result = get_departure(FLIGHTS_INFO[0]['departure_flight'], INPUT_DATA, 'straight')
    assert result == 'Sofia, SOF'


def test_get_arrival_straight():
    """
    Tests 'get_arrival' for straight flights.
    """
    result = get_arrival(FLIGHTS_INFO[0]['departure_flight'], INPUT_DATA, 'straight')
    assert result == 'Rome, CIA'


def test_get_departure_back():
    """
    Tests 'get_departure' for return flights.
    """
    result = get_departure(FLIGHTS_INFO[0]['arrival_flight'], INPUT_DATA, 'back')
    assert result == 'Rome, CIA'


def test_get_arrival_back():
    """
    Tests 'get_arrival' for return flights.
    """
    result = get_arrival(FLIGHTS_INFO[0]['arrival_flight'], INPUT_DATA, 'back')
    assert result == 'Sofia, SOF'


def test_get_duration():
    """
    Tests 'get_duration' for a flight.
    """
    result = get_duration(FLIGHTS_INFO[1]['departure_flight'])
    assert result == '45 min'


def test_get_flight_date():
    """
    Tests 'get_flight_date' extraction.
    """
    result = get_flight_date(FLIGHTS_INFO[0]['departure_flight'])
    assert result == datetime(2024, 9, 2, 0, 0)


def test_convert_date_format():
    """
    Tests 'convert_date_format' for proper formatting.
    """
    result = convert_date_format('Mon, Sep 2')
    assert result == 'Mon, Sep 02'


def test_get_departure_time():
    """
    Tests 'get_departure_time' extraction.
    """
    result = get_departure_time(FLIGHTS_INFO[0]['departure_flight'])
    assert result == datetime(2024, 9, 2, 13, 25)


def test_get_arrival_time():
    """
    Tests 'get_arrival_time' extraction.
    """
    result = get_arrival_time(FLIGHTS_INFO[0]['arrival_flight'])
    assert result == datetime(2024, 9, 3, 23, 20)
