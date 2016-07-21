"""
Provides the function that fully processes a range of hours
"""

from datetime import timedelta
import pandas as pd
from os import remove, listdir
from os.path import isfile

# Other required functions
from linktools import get_hours_list, get_download_link
from downloader import process_file

def process_range(start_time, end_time, append=False):
    """
    Downloads and processes hourly Wikipedia page traffic stats within a given time frame
    Backups are regularly saved to the hard drive in the form of csv files
    append allows to pick up from a previously generated csv file
    Inputs: start_time: 'YYYY-MM-DD-HH'
            end_time: 'YYYY-MM-DD-HH'
    """

    # create the list of all hours to be downloaded
    hourslist = get_hours_list(start_time, end_time)
    # format properly
    start_time = hourslist[0]
    end_time = hourslist[-1]
    total_hours = len(hourslist)
    skipped_hours = 0

    # append data to most recent file if so desired
    if append == True:
        # get the most recent file in the folder
        if isfile('error.log'):
            # prevent picking up the error log
            prev_filename = sorted(listdir())[-2]
        else:
            prev_filename = sorted(listdir())[-1]
        # create a new hourslist based on the new file
        start_time = prev_filename[-14:-10] + '-' + prev_filename[-10:-8] + '-' +\
                        prev_filename[-8:-6] + '-' + prev_filename[-6:-4]
        end_time = end_time.strftime('%Y-%m-%d-%H')
        # skip the first hour since that already exists on the hard drive
        hourslist = get_hours_list(start_time, end_time)[1:]
        start_time = hourslist[0]
        end_time = hourslist[-1]
        skipped_hours = total_hours - len(hourslist)
    
    # deal with one hour at a time
    for hours_done, hour in enumerate(hourslist):
        # create the link
        download_link = get_download_link(hour)
        # process the link and save the output to a data frame
        try:
            current_data = process_file(download_link)
        except:
            try:
                # sometimes the file name has a '1' (second) in the end
                download_link = list(download_link)
                download_link[-4] = '1'
                download_link = ''.join(download_link)
                current_data = process_file(download_link)
            except:
                try:
                    # sometimes the file name has a '5' (minute) in there
                    download_link = list(download_link)
                    download_link[-6] = '5'
                    download_link = ''.join(download_link)
                    current_data = process_file(download_link)
                except:
                    try:
                        # sometimes the file name has a '15' (minute) in there
                        download_link = list(download_link)
                        download_link[-6] = '5'
                        download_link[-7] = '1'
                        download_link = ''.join(download_link)
                        current_data = process_file(download_link)
                    except:
                        try:
                            # sometimes the file name has a '10' (minute) in there
                            download_link = list(download_link)
                            download_link[-7] = '1'
                            download_link = ''.join(download_link)
                            current_data = process_file(download_link)
                        except:
                            # out of ideas; make a note and move on
                            with open('error.log', 'a') as text:
                                problem_hour = hour.strftime('%Y-%m-%d-%H') + '\n'
                                text.write(problem_hour)
                            continue

        # add a column containing the hours
        current_data['hour'] = hour
        
        # save the results to a csv
        filename = 'data_up_to' + hour.strftime('%Y%m%d%H') + '.csv'
        if (hour == start_time) and (append == False):
            current_data.to_csv(filename, index=False)
            del current_data
        else:
            # Load previous data
            try:
                prev_data = pd.read_csv(prev_filename)
            except:
                try:
                    # in case the previous hour was skipped due to an error
                    prev_hour = hour - timedelta(hours=2)
                    prev_filename = 'data_up_to' + prev_hour.strftime('%Y%m%d%H') + '.csv'
                    prev_data = pd.read_csv(prev_filename)
                except:
                    # in case the previous two hours were skipped due to an error
                    prev_hour = hour - timedelta(hours=3)
                    prev_filename = 'data_up_to' + prev_hour.strftime('%Y%m%d%H') + '.csv'
                    prev_data = pd.read_csv(prev_filename)
            # Append current data
            new_data = prev_data.append(current_data)\
                        .reset_index(drop=True)\
                        .sort_values(by=['language', 'type', 'hour'])\
                        .reset_index(drop=True)
            # save the csv
            new_data.to_csv(filename, index=False)
            # clean up
            del prev_data, current_data, new_data
        
        # save the current file name for later to append lated data to it
        prev_filename = filename
        
        # status update: How far are we?
        percent_done = (hours_done + skipped_hours + 1) / total_hours * 100
        pretty_current_hour = hour.strftime('%Y-%m-%d %H:%M')
        status_update = 'Just finished with {latest}. That\'s {done} hour(s) so far ({perc}%).'
        status_print = status_update.format(latest=pretty_current_hour,
                                            done=hours_done + skipped_hours + 1,
                                            perc=round(percent_done, 1))
        print(status_print)

	    # have a rolling backup
        # always keep the last 5 files created
        if hours_done > 5:
            delete_hour = hour - timedelta(hours=6)
            delete_data = 'data_up_to' + delete_hour.strftime('%Y%m%d%H') + '.csv'
            try:
                remove(delete_data)
            except:
                print('No data deleted')
    return 'DONE!!!'
