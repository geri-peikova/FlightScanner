import re
from datetime import datetime

from date_utils import get_flight_date


class Flight:
    def __init__(self, flight_info, input_data, direction):
        """
        Initializes a Flight object with information about a specific flight.

        Parameters
        ----------
        flight_info : str
            The string containing details about the flight.
        input_data : dict
            A dictionary containing additional flight search parameters.
        direction : str
            The direction of the flight, either 'straight' or 'back'.
        """
        self.info = flight_info
        self.flight_from = get_departure(flight_info, input_data, direction)  # Sofia, SOF
        self.flight_to = get_arrival(flight_info, input_data, direction)      # Rome, CIA
        self.company = 'company'  # TODO: Update with actual company name
        self.departure_time = get_departure_time(flight_info)  # 'Mon, Sep 2, 1:25PM'
        self.arrival_time = get_arrival_time(flight_info)  # 'Mon, Sep 2, 2:10PM'
        self.duration = get_duration(flight_info)  # '1 hr 45 min'


class Travel:
    def __init__(self, flight_info, input_data):
        """
        Initializes a Travel object with information about the departure and arrival flights, price, and link.

        Parameters
        ----------
        flight_info : dict
            A dictionary containing details about the departure and arrival flights, price, and link.
        input_data : dict
            A dictionary containing additional flight search parameters.
        """
        self.departure_flight = Flight(flight_info['departure_flight'], input_data, 'straight')  # Departure flight details
        self.arrival_flight = Flight(flight_info['arrival_flight'], input_data, 'back')  # Arrival flight details
        self.price = flight_info['price']  # Price of the flight
        self.link = flight_info['link']  # Link to the flight booking page


def get_departure(flight_info, input_data, direction):
    """
    Extracts and returns the departure airport information from the flight info string.

    Parameters
    ----------
    flight_info : str
        The string containing details about the flight.
    input_data : dict
        A dictionary containing additional flight search parameters.
    direction : str
        The direction of the flight, either 'straight' or 'back'.

    Returns
    -------
    str
        The departure airport information.
    """
    departure = re.search(r'[A-Z]{3,}–[A-Z]{3,}', flight_info).group()
    if direction == 'straight':
        departure = input_data['flight_from'] + ', ' + departure.split('–')[0]
    else:
        departure = input_data['flight_to'] + ', ' + departure.split('–')[0]
    return departure


def get_arrival(flight_info, input_data, direction):
    """
    Extracts and returns the arrival airport information from the flight info string.

    Parameters
    ----------
    flight_info : str
        The string containing details about the flight.
    input_data : dict
        A dictionary containing additional flight search parameters.
    direction : str
        The direction of the flight, either 'straight' or 'back'.

    Returns
    -------
    str
        The arrival airport information.
    """
    arrival = re.search(r'[A-Z]{3,}–[A-Z]{3,}', flight_info).group()
    if direction == 'straight':
        arrival = input_data['flight_to'] + ', ' + arrival.split('–')[1]
    else:
        arrival = input_data['flight_from'] + ', ' + arrival.split('–')[1]
    return arrival


def get_duration(flight_info):
    """
    Extracts and returns the duration of the flight from the flight info string.

    Parameters
    ----------
    flight_info : str
        The string containing details about the flight.

    Returns
    -------
    str
        The duration of the flight.
    """
    duration = re.search(r'(\d+ hr( \d+ min)?)|((\d+ hr )?\d+ min)', flight_info).group()
    return duration


def get_departure_time(flight_info):
    """
    Extracts and returns the departure time of the flight from the flight info string.

    Parameters
    ----------
    flight_info : str
        The string containing details about the flight.

    Returns
    -------
    datetime
        The departure time of the flight.
    """
    departure_time = re.search(r'\d\d?:\d\d(.*?)(PM|AM)', flight_info).group()
    departure_time = departure_time.replace('\u202f', ' ')
    flight_date = get_flight_date(flight_info)
    departure_time = datetime.strptime(departure_time, '%I:%M %p')
    departure_time = flight_date.replace(hour=departure_time.hour, minute=departure_time.minute)
    return departure_time


def get_arrival_time(flight_info):
    """
    Extracts and returns the arrival time of the flight from the flight info string.

    Parameters
    ----------
    flight_info : str
        The string containing details about the flight.

    Returns
    -------
    datetime
        The arrival time of the flight.
    """
    arrival_time = re.split(r'\n – \n', flight_info)[1]
    arrival_time = re.search(r'\d\d?:\d\d(.*?)(PM|AM)', arrival_time).group()
    arrival_time = arrival_time.replace('\u202f', ' ')
    flight_date = get_flight_date(flight_info)
    arrival_time = datetime.strptime(arrival_time, '%I:%M %p')
    arrival_time = flight_date.replace(hour=arrival_time.hour, minute=arrival_time.minute)
    return arrival_time
