"""Setup data for testing"""

# pylint: disable=line-too-long
from flight_scanner.flight import Travel

INPUT_DATA = {
    'departure_weekday': 'Friday',
    'arrival_weekday': 'Sunday',
    'flight_from': 'Sofia',
    'flight_to': 'Rome',
    'dates_list': [{'End': 'Tue, Sep 3', 'Start': 'Mon, Sep 2'},
                   {'End': 'Tue, Sep 10', 'Start': 'Mon, Sep 9'},
                   {'End': 'Tue, Sep 17', 'Start': 'Mon, Sep 16'}]
}

FLIGHTS_INFO = [
    {
        'price': 'BGN 176',
        'departure_flight': 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions',
        'arrival_flight': 'Tue, Sep 3\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoy'
    },
    {
        'price': 'BGN 409',
        'departure_flight': 'Mon, Sep 2\n9:50\u202fPM\n – \n10:50\u202fPM\nWizz Air\n45 min\nSOF–FCO\n1h 55 min\n84 kg CO2e\n-8% emissions',
        'arrival_flight': 'Tue, Sep 3\n10:50\u202fAM\n – \n6:45\u202fPM\nLufthansa\n6 hr 55 min\nFCO–SOF\n1 stop\n3 hr 30 min MUC\n188 kg CO2e\n+107% emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpKEgoyMDI0LT'
    },
    {
        'price': 'BGN 590',
        'departure_flight': 'Mon, Sep 2\n6:40\u202fPM\n – \n9:25\u202fAM+1\nLOT\n15 hr 45 min\nSOF–FCO\n1 stop\n11 hr 40 min WAW\n244 kg CO2e\n+168% emissions',
        'arrival_flight': 'Tue, Sep 3\n7:40\u202fPM\n – \n1:55\u202fPM+1\nLOT\n17 hr 15 min\nFCO–SOF\n1 stop\n12 hr 50 min WAW\n244 kg CO2e\n+168% emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQAhpqEg'
    },
    {
        'price': 'BGN 239',
        'departure_flight': 'Mon, Sep 9\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\n-52% emissions',
        'arrival_flight': 'Tue, Sep 10\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=CBwA'
    },
    {
        'price': 'BGN 380',
        'departure_flight': 'Mon, Sep 9\n9:50\u202fPM\n – \n10:50\u202fPM\nWizz Air\n2 hr\nSOF–FCO\nNonstop\n84 kg CO2e\n-55% emissions',
        'arrival_flight': 'Tue, Sep 10\n10:50\u202fAM\n – \n11:00\u202fPM\nLufthansa\n11 hr 10 min\nFCO–SOF\n1 stop\n7 hr 45 min MUC\n170 kg CO2e\n+87% emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQA'
    },
    {
        'price': 'BGN 506',
        'departure_flight': 'Mon, Sep 9\n4:05\u202fPM\n – \n8:40\u202fPM\nAustrian\n5 hr 35 min\nSOF–FCO\n1 stop\n2 hr 30 min VIE\n173 kg CO2e\n-8% emissions',
        'arrival_flight': 'Tue, Sep 10\n8:55\u202fAM\n – \n3:20\u202fPM\nAustrian\n5 hr 25 min\nFCO–SOF\n1 stop\n2 hr 25 min VIE\n195 kg CO2e\n+114% emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=CBwQgA'
    },
    {
        'price': 'BGN 155',
        'departure_flight': 'Mon, Sep 16\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\n-52% emissions',
        'arrival_flight': 'Tue, Sep 17\n8:35\u202fPM\n – \n11:20\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nCIA–SOF\nNonstop\n91 kg CO2e\nAvg emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=g'
    },
    {
        'price': 'BGN 320',
        'departure_flight': 'Mon, Sep 16\n9:50\u202fPM\n – \n10:50\u202fPM\nWizz Air\n2 hr\nSOF–FCO\nNonstop\n84 kg CO2e\n-55% emissions',
        'arrival_flight': 'Tue, Sep 17\n8:55\u202fAM\n – \n3:20\u202fPM\nAustrian\n5 hr 25 min\nFCO–SOF\n1 stop\n2 hr 25 min VIE\n195 kg CO2e\n+114% emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=Ccg'
    },
    {
        'price': 'BGN 499',
        'departure_flight': 'Mon, Sep 16\n12:55\u202fPM\n – \n6:15\u202fPM\nLufthansa\n6 hr 20 min\nSOF–FCO\n1 stop\n2 hr 50 min MUC\n195 kg CO2e\nAvg emissions',
        'arrival_flight': 'Tue, Sep 17\n10:50\u202fAM\n – \n6:45\u202fPM\nLufthansa\n6 hr 55 min\nFCO–SOF\n1 stop\n3 hr 30 min MUC\n188 kg CO2e\n+107% emissions',
        'link': 'https://www.google.com/travel/flights/booking?tfs=0wOS'
    }
]

LIST_FLIGHTS_UNSORTED = [
    Travel(flight_info, INPUT_DATA) for flight_info in FLIGHTS_INFO
]
