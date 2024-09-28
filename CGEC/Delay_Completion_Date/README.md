Guide for using Delay_Completion_Date folder:

This python program aim to read the latest completion date and no. of affected workdays in specific cells of excel file,
and write steps and result (revised completion date) into specific cells.
Please note that there will be multiple latest completion date due to different parts of a project.

The excel file should have the following structure:
1. number of parts                              (e.g. cell B3 to B11, 9 parts in total)
2. latest completion dates for different parts  (e.g. cell D3 to D11)
3. affected workdays for different parts        (e.g. cell E3 to E11)
4. steps for different parts                    (e.g. cell F3 to F11)
5. revised completion date for different parts  (e.g. cell G3 to G11)

You might use '''Delay Completion Date.xlsx''' as Reference.

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

Examlple:

    e.g. latest completion date = 2023-12-30 (Sat), affected workdays = 3
    2023-12-30 is a Saturday, set counter = 0
    the next day 2023-12-31 is a Sunday, which is not a workday, so we do not add 1 to counter.
    the next day 2024-01-01 is a holiday, which is not a workday, so we do not add 1 to counter.
    the next day 2024-01-02 is a workday, add 1 to counter. counter = 1.
    the next day 2024-01-03 is a workday, add 1 to counter. counter = 2.
    the next day 2024-01-04 is a workday, add 1 to counter. counter = 3.
    Now the affected workdays are all accounted for, the revised completion date is 2024-01-04.