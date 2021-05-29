import os
os.getcwd()
os.chdir('C:/Users/okiem/github/mlb-dfs')
from mlb_scraper import YahooScrape


ys = YahooScrape()

ys.get_recent_contests()
ys.compare_contests()
ys.update_master_dct()
