"""
Provides the function to download and process a file of hourly Wikipedia traffic
"""

from io import BytesIO
from urllib.request import urlopen
import gzip

# other required functions
from batch_data_read import batch_data_read
from aggregation import aggregate_hour

def process_file(download_link):
    """
    Downloads the file for a given day
    Processes everything and aggregates all hits to language levels (distinguishing between mobile and non-mobile traffic)
    Returns a Pandas DataFrame
    Input: Download link
    """
    with urlopen(download_link) as archive:
        with gzip.open(BytesIO(archive.read())) as f:
            file_content = f.read()
    file_content = file_content.decode('utf-8', errors='ignore')
    file_content = file_content.split('\n')
    # A separate function the processes this list of stats
    dat = batch_data_read(file_content, 1000000)
    # free up some memory
    del file_content
    # aggregate the current hour
    dat = aggregate_hour(dat)
    
    return dat
