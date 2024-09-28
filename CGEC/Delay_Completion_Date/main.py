"""
This python file aim to read the latest completion date in specific cells of excel file,
and write steps and result (revised completion date) into specific cells.  
Please note that there will be multiple latest completion date due to different parts of a project.

The excel file should have the following structure:
1. number of parts                              (e.g. cell B3 to B11, 9 parts in total)
2. latest completion dates for different parts  (e.g. cell D3 to D11)
3. affected workdays for different parts        (e.g. cell E3 to E11)
4. steps for different parts                    (e.g. cell F3 to F11)
5. revised completion date for different parts  (e.g. cell G3 to G11)
"""

import tkinter as tk
from tkinter import simpledialog, filedialog
import openpyxl
from datetime import datetime
from delay_to_completion_date import calculate_revised_completion_date
from openpyxl.styles import Alignment

def open_file_explorer():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select the template Excel file", filetypes=[("Excel files", "*.xlsx")])
    return file_path

def get_number_of_parts():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    number_of_parts = simpledialog.askinteger("Input", "Enter the number of parts:")
    return number_of_parts

# Example usage
template_path = open_file_explorer()
number_of_parts = get_number_of_parts()

# Load the Excel file
wb = openpyxl.load_workbook(template_path)
sheet = wb.active

# Define the starting cells for the data
latest_completion_date_start_cell = 'D3'
affected_workdays_start_cell = 'E3'
steps_start_cell = 'F3'
revised_completion_date_start_cell = 'G3'

# Read the latest completion dates and affected workdays
latest_completion_dates = []
affected_workdays_list = []
for i in range(number_of_parts):
    date_cell = f'{latest_completion_date_start_cell[0]}{int(latest_completion_date_start_cell[1:]) + i}'
    workdays_cell = f'{affected_workdays_start_cell[0]}{int(affected_workdays_start_cell[1:]) + i}'

    date_value = sheet[date_cell].value
    if isinstance(date_value, datetime):
        latest_completion_dates.append(date_value.date())
    else:
        latest_completion_dates.append(datetime.strptime(date_value, '%m/%d/%Y').date())
    affected_workdays_list.append(sheet[workdays_cell].value)

# print(latest_completion_dates)
# print(affected_workdays_list) # works as expected

# Calculate revised completion dates and write the results
for i in range(number_of_parts):
    latest_completion_date = latest_completion_dates[i]
    affected_workdays = affected_workdays_list[i]
    result = calculate_revised_completion_date(latest_completion_date, affected_workdays)
    revised_date = result['date']
    steps = result['steps']
    # print(f"Part {i + 1}: Revised completion date: {revised_date}")
    # print("Steps: ", steps)

    # Write the revised completion date
    revised_date_cell = f'{revised_completion_date_start_cell[0]}{int(revised_completion_date_start_cell[1:]) + i}'
    sheet[revised_date_cell] = revised_date.strftime('%Y-%m-%d')

    # Concatenate the steps into a single string
    steps_str = "\n".join([f"{step[0].strftime('%Y-%m-%d')}: {step[1]}" for step in steps])

    # Write the steps
    steps_cell = f'{steps_start_cell[0]}{int(steps_start_cell[1:]) + i}'
    sheet[steps_cell] = steps_str
    sheet[steps_cell].alignment = Alignment(wrap_text=True)

# Save the updated Excel file
wb.save('delay_completion_date.xlsx')