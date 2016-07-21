"""
Provides a function that aggregates hourly data
"""

# careful when using this: type mw always has count = 1

import pandas as pd

def aggregate_hour(dat):
    """
    Aggregates all articles grouped by type and language
    Returns the number of visits, amount of traffic, and number
    of articles accessed per type and language
    """
    groups = dat.groupby(['language', 'type'])
    out_df = groups.agg('sum')\
            .join(pd.DataFrame(groups.size(), columns=['count']))\
            .reset_index()
    
    return out_df
