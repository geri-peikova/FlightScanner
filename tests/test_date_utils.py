from datetime import datetime
from freezegun import freeze_time
import pytest
from date_utils import get_travel_dates, convert_date_format, format_datetime_to_textdate_and_time, get_flight_date


def get_weekday_index(day):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days.index(day)


@pytest.fixture(autouse=True)
def mock_get_weekday_index(monkeypatch):
    monkeypatch.setattr('date_utils.get_weekday_index', get_weekday_index)


@freeze_time("2024-05-20")
def test_get_travel_dates_one_month():
    start_day = 'Monday'
    end_day = 'Friday'
    expected_output = [{'End': 'Fri, May 24', 'Start': 'Mon, May 20'},
                       {'End': 'Fri, May 24', 'Start': 'Mon, May 20'},
                       {'End': 'Fri, May 31', 'Start': 'Mon, May 27'},
                       {'End': 'Fri, May 31', 'Start': 'Mon, May 27'},
                       {'End': 'Fri, Jun 07', 'Start': 'Mon, Jun 03'},
                       {'End': 'Fri, Jun 07', 'Start': 'Mon, Jun 03'},
                       {'End': 'Fri, Jun 14', 'Start': 'Mon, Jun 10'},
                       {'End': 'Fri, Jun 14', 'Start': 'Mon, Jun 10'}]
    assert get_travel_dates(start_day, end_day, num_months=1) == expected_output


@freeze_time("2024-05-20")
def test_get_travel_dates_ending_in_next_week():
    start_day = 'Sunday'
    end_day = 'Wednesday'
    expected_output = [{'End': 'Wed, May 29', 'Start': 'Sun, May 26'},
                       {'End': 'Wed, May 29', 'Start': 'Sun, May 26'},
                       {'End': 'Wed, Jun 05', 'Start': 'Sun, Jun 02'},
                       {'End': 'Wed, Jun 05', 'Start': 'Sun, Jun 02'},
                       {'End': 'Wed, Jun 12', 'Start': 'Sun, Jun 09'},
                       {'End': 'Wed, Jun 12', 'Start': 'Sun, Jun 09'},
                       {'End': 'Wed, Jun 19', 'Start': 'Sun, Jun 16'},
                       {'End': 'Wed, Jun 19', 'Start': 'Sun, Jun 16'}]
    assert get_travel_dates(start_day, end_day) == expected_output


def test_get_weekday_index():
    assert get_weekday_index('Monday') == 0
    assert get_weekday_index('Tuesday') == 1
    assert get_weekday_index('Wednesday') == 2
    assert get_weekday_index('Thursday') == 3
    assert get_weekday_index('Friday') == 4
    assert get_weekday_index('Saturday') == 5
    assert get_weekday_index('Sunday') == 6


def test_format_datetime_to_textdate_and_time():
    dt = datetime(2024, 5, 25, 15, 30)
    expected_output = "25 May 2024, 15:30h"
    assert format_datetime_to_textdate_and_time(dt) == expected_output


def test_convert_date_format_single_digit_day():
    assert convert_date_format('Mon, Sep 2') == 'Mon, Sep 02'
    assert convert_date_format('Tue, Oct 5') == 'Tue, Oct 05'


def test_convert_date_format_double_digit_day():
    assert convert_date_format('Mon, Sep 12') == 'Mon, Sep 12'
    assert convert_date_format('Tue, Oct 13') == 'Tue, Oct 13'


def test_get_flight_date():
    flight_info = 'Mon, Sep 2\n1:25\u202fPM\n – \n2:10\u202fPM\nRyanairOperated by Ryanair Sun\n1 hr 45 min\nSOF–CIA\nNonstop\n91 kg CO2e\nAvg emissions'
    assert get_flight_date(flight_info) == datetime(2024, 9, 2, 0, 0)