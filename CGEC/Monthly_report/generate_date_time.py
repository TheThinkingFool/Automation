'''
Part 2: Generate Random Date and Time
    generate a random date and time for each photo, i.e. date = {random DD}/MM/YYYY,
    time = {random hh}:{random mm} from 09:00 to 16:59. ask the MM/YYYY of monthly progress photo from the user.
1. Ask the user for the MM/YYYY of the monthly progress photo.
2. Generate a random date and time for each photo within the specified range.
3. Return the generated date and time data.
'''

import tkinter as tk
from tkinter import simpledialog
import random
from datetime import datetime, timedelta

def get_month_year():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    month_year = simpledialog.askstring("Input", "Enter the MM/YYYY of the monthly progress photo:")
    return month_year

# format: DD/MM/YYYY HH/MM, e.g. 31/01/2024 13:59
def generate_random_date_time(month_year, num_photos):
    month, year = map(int, month_year.split('/'))
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    date_times = []
    for _ in range(num_photos):
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        random_time = random.randint(9 * 60, 16 * 60 + 59)  # Minutes from 09:00 to 16:59
        random_hour = random_time // 60
        random_minute = random_time % 60
        date_time = random_date.replace(hour=random_hour, minute=random_minute)
        date_times.append(date_time.strftime("%d/%m/%Y %H:%M"))

    return date_times
