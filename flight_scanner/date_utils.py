import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def get_travel_dates(start_day, end_day, num_months=1):
    """
    Generates a list of travel dates within the specified number of months.

    Parameters
    ----------
    start_day : str
        The starting day of the week for travel (e.g., 'Monday').
    end_day : str
        The ending day of the week for travel (e.g., 'Friday').
    num_months : int, optional
        The number of months within which to generate travel dates (default is 1).

    Returns
    -------
    travel_dates_list : list
        A list of dictionaries, each containing 'Start' and 'End' keys with travel dates.
    """
    start_day = get_weekday_index(start_day)
    end_day = get_weekday_index(end_day)
    travel_dates_list = []
    today = datetime.now()

    current_day_of_week = today.weekday()
    days_until_start_day = (start_day - current_day_of_week + 7) % 7
    next_weekday = today + timedelta(days=days_until_start_day)

    while next_weekday + timedelta(days=end_day) <= today + relativedelta(
            months=+num_months):
        if start_day >= end_day:
            week_set = {
                'End': (next_weekday + timedelta(days=end_day) - timedelta(start_day - 7)).strftime('%a, %b %d')}
        else:
            week_set = {'End': (next_weekday + timedelta(days=end_day)).strftime('%a, %b %d')}
        week_set['Start'] = next_weekday.strftime('%a, %b %d')
        travel_dates_list.append(week_set)
        travel_dates_list.append(week_set)
        next_weekday += timedelta(days=7)
    return travel_dates_list


def get_weekday_index(weekday):
    """
    Returns the index of the given weekday.

    Parameters
    ----------
    weekday : str
        The name of the weekday (e.g., 'Monday').

    Returns
    -------
    index : int
        The index of the weekday (0 for Monday, 6 for Sunday).
    """
    for index, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
        if day == weekday:
            return index


def format_datetime_to_textdate_and_time(dt):
    """
    Formats a datetime object to a string in the given format.

    Parameters
    ----------
    dt : datetime
        Datetime.

    Returns
    -------
    dt : str
        The formatted date and time string.
    """
    dt = dt.strftime("%d %b %Y, %H:%Mh")
    return dt


def convert_date_format(flight_date):   # "Mon, Sep 2"
    """
    Converts a flight date string to ensure the day part is two digits.

    Parameters
    ----------
    flight_date : str
        The flight date string (e.g., 'Mon, Sep 2').

    Returns
    -------
    flight_date : str
        The converted flight date string (e.g., 'Mon, Sep 02').
    """
    flight_date = flight_date.split(' ')
    if len(flight_date[-1]) == 1:
        flight_date[-1] = '0' + flight_date[-1]
    flight_date = ' '.join(flight_date)
    return flight_date


def get_flight_date(flight_info):
    """
    Extracts and returns the flight date from the flight info string.

    Parameters
    ----------
    flight_info : str
        The string containing details about the flight.

    Returns
    -------
    current_date : datetime
        The flight date as a datetime object.
    """
    flight_date_string = re.search(r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d+', flight_info).group()    # "Mon, Sep 2"
    flight_date_string = convert_date_format(flight_date_string)
    flight_date = datetime.strptime(flight_date_string, '%a, %b %d')
    current_year = datetime.now().year
    while True:
        current_date = datetime(current_year, flight_date.month, flight_date.day)
        if current_date.strftime("%a, %b %d") == flight_date_string:
            return current_date
        current_year += 1
