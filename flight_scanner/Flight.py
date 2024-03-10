class Flight:
    def __init__(self, departure, arrival, company, departure_time, arrival_time, duration, price):
        self.departure = departure
        self.arrival = arrival
        self.company = company
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.price = price



""" 
    {
    'price': 'BGN 176', 
    'departure_flight': 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions', 
    'arrival_flight': 'Tue, Sep 3\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions', 
    'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'
    }
"""