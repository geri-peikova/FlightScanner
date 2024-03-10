import re


class Flight:
    def __init__(self, flight_info, input_data):
        self.departure = get_departure(flight_info, input_data)  # Sofia, SOF
        self.arrival = get_arrival(flight_info, input_data)      # Rome, CIA
        self.company = 'company'      # TODO: Ryanair
        self.departure_time = 'departure_time'    # 'Mon, Sep 2, 1:25PM
        self.arrival_time = 'arrival_time'    # 'Mon, Sep 2, 2:10PM
        self.duration = 'duration'    # 1 hr 45 min


class Travel:
    def __init__(self, flight_info, input_data):
        self.departure_flight = Flight(flight_info['departure_flight'], input_data)     # 'departure_flight': 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions'
        self.arrival_flight = Flight(flight_info['arrival_flight'], input_data)   # 'arrival_flight': 'Tue, Sep 3\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions'
        self.price = flight_info['price']  # BGN 176
        self.link = flight_info['link']  # 'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'


def get_departure(flight_info, input_data):
    departure = re.search(r'[A-Z]{3,}–[A-Z]{3,}', flight_info).group()
    departure = input_data['flight_from'] + ', ' + departure.split('–')[0]
    return departure


def get_arrival(flight_info, input_data):
    arrival = re.search(r'[A-Z]{3,}–[A-Z]{3,}', flight_info).group()
    arrival = input_data['flight_to'] + ', ' + arrival.split('–')[0]
    return arrival


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