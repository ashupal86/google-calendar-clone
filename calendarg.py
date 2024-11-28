from datetime import datetime
import calendar

def generate_month_calendar(year, month):
    # Get the first day of the month and the number of days in the month
    first_day, num_days = calendar.monthrange(year, month)

    # Initialize the weeks list
    weeks = []
    week = [0] * first_day  # Start the first week with empty days (0s)

    # Fill in the days of the month
    for day in range(1, num_days + 1):
        week.append(day)
        if len(week) == 7:  # If the week has 7 days, push it and reset the week
            weeks.append(week)
            week = []

    # Add the last week if it has any remaining days
    if week:
        while len(week) < 7:  # Fill remaining spaces with 0s if the week isn't complete
            week.append(0)
        weeks.append(week)

    return weeks

# Example usage for the current month
today = datetime.today()
month_calendar = generate_month_calendar(today.year, today.month)
print(month_calendar)  # Output for checking the structure
