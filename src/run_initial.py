import os
os.getcwd()
os.chdir('C:/Users/okiem/github/mlb-dfs')
from mlb_scraper import YahooScrape


ys = YahooScrape()

ys.create_dir()
ys.create_contests_dct()
ys.insert_master_dct()
ys.create_scheduled_task()
