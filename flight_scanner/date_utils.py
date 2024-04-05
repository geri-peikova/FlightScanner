from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


def generate_dates(start_day, end_day, num_months=1):
    start_day = get_index_by_weekday_name(start_day)
    end_day = get_index_by_weekday_name(end_day)
    dates_list = []
    today = datetime.now()

    # Find the next Friday
    current_day_of_week = today.weekday()
    days_until_start_day = (start_day - current_day_of_week + 7) % 7
    next_weekday = today + timedelta(days=days_until_start_day)

    # Print all the dates starting from Friday and ending on Monday for the next two months
    while next_weekday + timedelta(days=end_day) <= today + relativedelta(
            months=+num_months):  # Print for the next two months (8 weeks)
        if start_day >= end_day:
            week_set = {
                'End': (next_weekday + timedelta(days=end_day) - timedelta(start_day - 7)).strftime('%a, %b %d')}
        else:
            week_set = {'End': (next_weekday + timedelta(days=end_day)).strftime('%a, %b %d')}
        week_set['Start'] = next_weekday.strftime('%a, %b %d')
        dates_list.append(week_set)
        next_weekday += timedelta(days=7)
    return dates_list


def get_index_by_weekday_name(weekday):
    for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
        if day == weekday:
            return i


def get_calendar_dates():

    today = datetime.today()
    next_year = today + timedelta(days=183)

    weekend_dates = []
    current_weekend = []

    day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    current_date = today
    while current_date <= next_year:
        if current_date.weekday() in (4, 5, 6):
            current_weekend.append(f"{current_date.strftime('%d.%m.%Y')} ({day_labels[current_date.weekday()]})")
        if current_date.weekday() == 6:  # If the current date is Sunday, it's the end of the weekend
            if current_weekend:  # Check if there are dates in the current weekend
                weekend_dates.append(current_weekend)
                current_weekend = []  # Reset the current weekend
        current_date += timedelta(days=1)

    for i, weekend in enumerate(weekend_dates, start=1):
        print(f"Weekend {i}:")
        for date in weekend:
            print(date)
        print()


def format_datetime_to_textdate_and_time(dt):
    return dt.strftime("%d %b %Y, %H:%Mh")
