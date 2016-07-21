"""
This is a command line wrapper to run the 'main' programm
"""

from main import process_range

start_time = input('Enter the first hour. The format is YYYY-MM-DD-HH: ')
end_time = input('Enter the last hour. The format is YYYY-MM-DD-HH: ')
append = input('Append to previous data in the folder? (Yes/No): ')
append = (append == 'Yes')

process_range(start_time, end_time, append)
