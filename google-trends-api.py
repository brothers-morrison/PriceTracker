r"""
.SYNOPSIS
	This code taken shamelessly from
.LINK
	https://dev.to/oxylabs-io/how-to-get-data-from-google-trends-using-python-4958
"""

import pytrends
# pip install pytrends
import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt


#TBD: make the search an argument to the program/function
QUERY = 'Python'
OUTFILE = 'google_trends_data.csv'



#provide your search terms
kw_list=['"Ralph" loop', 'ai context size']

#search interest per region
#run model for keywords (can also be competitors)
pytrend = TrendReq()

# timeframe options
# "today 1-d"
# "today 1-w"
# "today 1-m"
# "today 1-y"
# timeframe='2020-01-01 2020-01-31'
pytrend.build_payload(kw_list, timeframe='today 1-y')


def interest_by_region():
    # Interest by Region
    regiondf = pytrend.interest_by_region()
    #looking at rows where all values are not equal to 0
    regiondf = regiondf[(regiondf != 0).all(1)]

    #drop all rows that have null values in all columns
    regiondf.dropna(how='all',axis=0, inplace=True)
    regiondf = regiondf.sort_values(by=kw_list[0],ascending=False)
    
    #visualise -- #TBD this isn't working at all. 
    regiondf.plot(figsize=(20, 12), y=kw_list, kind ='bar')
    print(regiondf)
    
    try:
        regiondf.to_csv(OUTFILE)
    finally:
        return

"""
    UNTESTED
"""
def historical_interest(year_start="2020", month_start=10, day_start=1, hour_start=0, year_end=2021, month_end=10, day_end=1, hour_end=0):
    #historical interest
    historicaldf = pytrend.get_historical_interest(kw_list, "year_start="+year_start, month_start=10, day_start=1, hour_start=0, year_end=2021, month_end=10, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
    return


interest_by_region()


