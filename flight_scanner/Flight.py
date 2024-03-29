import re
from datetime import datetime


class Flight:
    def __init__(self, flight_info, input_data, direction):
        self.info = flight_info
        self.flight_from = get_departure(flight_info, input_data, direction)  # Sofia, SOF
        self.flight_to = get_arrival(flight_info, input_data, direction)      # Rome, CIA
        self.company = 'company'      # TODO: Ryanair
        self.departure_time = get_departure_time(flight_info)    # 'Mon, Sep 2, 1:25PM
        self.arrival_time = get_arrival_time(flight_info)    # 'Mon, Sep 2, 2:10PM
        self.duration = get_duration(flight_info)    # 1 hr 45 min


class Travel:
    def __init__(self, flight_info, input_data):
        self.departure_flight = Flight(flight_info['departure_flight'], input_data, 'straight')     # 'departure_flight': 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions'
        self.arrival_flight = Flight(flight_info['arrival_flight'], input_data, 'back')   # 'arrival_flight': 'Tue, Sep 3\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions'
        self.price = flight_info['price']  # BGN 176
        self.link = flight_info['link']  # 'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'


def get_departure(flight_info, input_data, direction):
    departure = re.search(r'[A-Z]{3,}–[A-Z]{3,}', flight_info).group()
    if direction == 'straight':
        departure = input_data['flight_from'] + ', ' + departure.split('–')[0]
    else:
        departure = input_data['flight_to'] + ', ' + departure.split('–')[0]
    return departure


def get_arrival(flight_info, input_data, direction):
    arrival = re.search(r'[A-Z]{3,}–[A-Z]{3,}', flight_info).group()
    if direction == 'straight':
        arrival = input_data['flight_to'] + ', ' + arrival.split('–')[1]
    else:
        arrival = input_data['flight_from'] + ', ' + arrival.split('–')[1]
    return arrival


def get_duration(flight_info):
    duration = re.search(r'(\d+ hr( \d+ min)?)|((\d+ hr )?\d+ min)', flight_info).group()
    return duration


def get_flight_date(flight_info):
    flight_date_string = re.search(r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d+', flight_info).group()    # "Mon, Sep 2"
    flight_date_string = convert_date_format(flight_date_string)
    flight_date = datetime.strptime(flight_date_string, '%a, %b %d')
    current_year = datetime.now().year
    while True:
        current_date = datetime(current_year, flight_date.month, flight_date.day)
        if current_date.strftime("%a, %b %d") == flight_date_string:
            return current_date
        current_year += 1


def convert_date_format(flight_date):   # "Mon, Sep 2"
    flight_date = flight_date.split(' ')
    if len(flight_date[-1]) == 1:
        flight_date[-1] = '0' + flight_date[-1]
    flight_date = ' '.join(flight_date)
    return flight_date


def get_departure_time(flight_info):
    departure_time = re.search(r'\d\d?:\d\d(.*?)(PM|AM)', flight_info).group()
    departure_time = departure_time.replace('\u202f', ' ')
    flight_date = get_flight_date(flight_info)
    departure_time = datetime.strptime(departure_time, '%I:%M %p')
    departure_time = flight_date.replace(hour=departure_time.hour, minute=departure_time.minute)
    return departure_time


def get_arrival_time(flight_info):
    arrival_time = re.split(r'\n – \n', flight_info)[1]
    arrival_time = re.search(r'\d\d?:\d\d(.*?)(PM|AM)', arrival_time).group()
    arrival_time = arrival_time.replace('\u202f', ' ')
    flight_date = get_flight_date(flight_info)
    arrival_time = datetime.strptime(arrival_time, '%I:%M %p')
    arrival_time = flight_date.replace(hour=arrival_time.hour, minute=arrival_time.minute)
    return arrival_time
