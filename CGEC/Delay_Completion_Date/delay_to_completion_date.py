"""
input - latest completion date + affected workdays
processing - for i in range(no. of affected workdays):
                start from latest completion date,
                check if next date is holiday or Sunday,
                    if yes, i+=1.
output - revised completion date

definition:
    latest completion date:
        the delayed date for the completion of a task,
        due to the latest compensation event (CE).

    affected workdays:
        the number of workdays affected by the latest CE,
        in which workdays only excludes holidays and Sundays.

    revised completion date:
        the revised date for the completion of a task,
        after taking into account the current CE.

    e.g. latest completion date = 2023-12-30 (Sat), affected workdays = 3
    2023-12-30 is a Saturday, set counter = 0
    the next day 2023-12-31 is a Sunday, which is not a workday, so we do not add 1 to counter.
    the next day 2024-01-01 is a holiday, which is not a workday, so we do not add 1 to counter.
    the next day 2024-01-02 is a workday, add 1 to counter. counter = 1.
    the next day 2024-01-03 is a workday, add 1 to counter. counter = 2.
    the next day 2024-01-04 is a workday, add 1 to counter. counter = 3.
    Now the affected workdays are all accounted for, the revised completion date is 2024-01-04.

"""

from datetime import date, timedelta
from check_workday import is_workday

def calculate_revised_completion_date(latest_completion_date, affected_workdays):
    _date = latest_completion_date
    workdays_counted = 0
    steps = []

    while workdays_counted < affected_workdays:
        _date += timedelta(days=1)
        is_workday_flag, reason = is_workday(_date)
        if is_workday_flag:
            workdays_counted += 1
            steps.append((_date, workdays_counted))
        else:
            steps.append((_date, reason))

    return {
        "date": _date,
        "steps": steps
    }

def test_calculate_revised_completion_date(): # works as expected
    latest_completion_date = date(2023, 12, 30)
    affected_workdays = 3
    result = calculate_revised_completion_date(latest_completion_date, affected_workdays)
    print(f"Revised completion date: {result['date']}")  # Output: 2024-01-04
    print("Steps:")
    for step in result["steps"]:
        print(f"{step[0]}     {step[1]}")