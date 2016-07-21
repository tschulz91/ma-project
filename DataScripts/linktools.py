"""
Provides function to create the list of hours (and dates) for which to download traffic stats
Provides function to create the download link from a given date-hour combo
"""

from datetime import datetime, timedelta
from numpy import linspace

def get_hours_list(start_time, end_time):
    """
    Returns the list of dates/hours to download
    Inputs: start_time: 'YYYY-MM-DD-HH'
            end_time: 'YYYY-MM-DD-HH'
    """
    start_hour, end_hour = datetime.strptime(start_time, '%Y-%m-%d-%H'), datetime.strptime(end_time, '%Y-%m-%d-%H')
    # Calculate the range
    time_range = end_hour - start_hour
    # Express the range in number of hours
    range_hours = int(time_range.days * 24 + time_range.seconds / 3600)
    # Create a linespace of one hour increments between start_time and end_time
    linespace =  timedelta(hours=1) * linspace(0, range_hours, num=range_hours+1)
    timeline = start_hour + linespace
    return timeline

def get_download_link(date_hour):
    """
    Returns the URL for the download of traffic stats for a given hour of a given day
    Input: datetime object
    """
    base_url = 'https://dumps.wikimedia.org/other/pagecounts-raw/{year}/{year}-{month}/pagecounts-{year}{month}{day}-{hour}0000.gz'
    download_url = base_url.format(year=date_hour.strftime('%Y'),
                                   month=date_hour.strftime('%m'),
                                   day=date_hour.strftime('%d'),
                                   hour=date_hour.strftime('%H'))
    return download_url
