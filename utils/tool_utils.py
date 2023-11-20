""" Define the tools that the assistant can use """
from typing import List
from pytrends.request import TrendReq
# Define the "get_trends_data" tool
# Which uses the pytrends library to get Google Trends data
def get_trends_data(keywords: List[str], timeframe: str, geo: str):
    """ Get Google Trends data """
    # Establish "PR" as a constant keyword
    keyword_list = ["PR"]
    keyword_list += keywords
    trends = TrendReq(hl='en-US', tz=360)
    trends.build_payload(keyword_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
    df = trends.interest_over_time()
    return df.to_json()