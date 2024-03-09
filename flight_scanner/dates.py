from datetime import datetime, timedelta, date


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


if __name__ == '__main__':
    get_calendar_dates()