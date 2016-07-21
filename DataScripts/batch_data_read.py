from numpy import nan
import pandas as pd

# import required functions from other scripts
from process_line import process_line

def batch_data_read(dat, batch_size):
    """
    Process the data in batches of `batch_size` to keep memory usage down
    """
    total_size = len(dat)
    batch_start = 0
    return_df = pd.DataFrame([], columns=['language', 'type', 'article', 'visits', 'traffic'])
    while batch_start < (total_size-1):
        batch_end = min(batch_start+int(batch_size), total_size)
        # ugly fix: if unzipping results in an empty line in the end, do not consider it
        if len(dat[batch_end-1]) == 0: batch_end = batch_end - 1
        temp_df = pd.DataFrame([process_line(line, line_number) for line_number, line in enumerate(dat[batch_start:batch_end])],
                               columns=['lang_type', 'article', 'visits', 'traffic'])
        new_cols = list(temp_df.lang_type.str.split('.'))
        # Add type 'wiki' when no type is defined
        new_cols = [[line[0], 'wiki'] if len(line)==1 else line for line in new_cols]
        new_cols = pd.DataFrame(new_cols, columns=['language', 'type'])
        temp_df['language'], temp_df['type'] = new_cols['language'], new_cols['type']
        return_df = return_df.append(temp_df[['language', 'type', 'article', 'visits', 'traffic']],
                                     ignore_index=True)
        # free up some memory
        del temp_df
        
        batch_start = batch_end
    return return_df
