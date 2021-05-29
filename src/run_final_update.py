import os
os.getcwd()
os.chdir('C:/Users/okiem/github/mlb-dfs')
from mlb_scraper import YahooScrape


ys = YahooScrape()

ys.create_contestid_lst()
ys.create_entryid_lst()
