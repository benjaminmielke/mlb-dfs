from datetime import datetime
import json
import urllib.request
import os
import logging
from collections import OrderedDict
import time
# ------------------------------------------------------------------------------

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger
 
# Create loggers
logger_info = setup_logger('logger_info', f'C:/Users/okiem/github/mlb-dfs/logs/mlb_scaper_infolog_{datetime.today().strftime("%Y%m%d")}.log')
logger_error = setup_logger('logger_error', f'C:/Users/okiem/github/mlb-dfs/logs/mlb_scaper_errorlog_{datetime.today().strftime("%Y%m%d")}.log')


class ScrapeToolbelt():
    '''
    '''

    def __init__(self):
        '''
        '''
        self.path_proj = 'C:/Users/okiem/github/mlb-dfs'
# ------------------------------------------------------------------------------

    def get_json(self, url):
        '''
        '''
        try:
            url_req = urllib.request.urlopen(url, timeout=20)
            #logger_info.info(f'in STB -----------> SUCCESS: get_json() ... Connected to {url}')
        except urllib.error.HTTPError:
            logger_error.exception(f'in STB -----------> WARNING: get_json() ... Unable to connect to {url}')
            print('uhoh')
            pass
        except TimeoutError:
            logger_error.exception(f'in STB -----------> WARNING: get_json() ... Unable to connect to {url}')
            print('uhoh2')
            time.sleep(20)
            pass
        except OSError:
            logger_error.exception(f'in STB -----------> WARNING: get_json() ... Unable to connect to {url}')
            print('uhoh2')
            time.sleep(20)
            pass
        data = json.loads(url_req.read().decode())

        return data
# ------------------------------------------------------------------------------

    def dump_json(self, dct, filename=None, date=datetime.today().strftime('%Y-%m-%d')):
        '''
        '''
        try:
            with open(f'{self.path_proj}/data/{date}/{filename}.json', 'w') as f:
                json.dump(dct,
                          f,
                          ensure_ascii=False)
            logger_info.info(f'in STB -----------> SUCCESS: dump_json() ... master_dct inserted into {self.path_proj}/data/{date}/{filename}.json')
        except:
            logger_error.exception('See exception.')


# ------------------------------------------------------------------------------

    def open_json(self, filename=None, date=datetime.today().strftime('%Y-%m-%d')):
        '''
        '''
        try:
            with open(f'{self.path_proj}/data/{date}/{filename}.json') as data:
                dct = json.load(data)
            logger_info.info(f'in STB -----------> SUCCCESS: open_json() ... dct loaded from {self.path_proj}/data/{date}/{filename}.json')
        except:
            logger_error.exception(f'in STB -----------> FAILED loading dct from {self.path_proj}/data/{date}/{filename}.json')

        return dct
# ------------------------------------------------------------------------------

    def create_lst(self, dct=None, key=None):
        '''
        '''
        lst = []
        for index, contest in enumerate(dct.get('contests').get('result')):
            lst.append(contest.get(f'{key}'))

        if lst:
            logger_info.info(f'in STB -----------> SUCCESS: create_lst() ... list created using {key} key')
        else:
            logger_error.warning(f'in STB -----------> WARNING: create_lst() ... list is empty using {key} key. Investigate.')

        return lst



# ________________________________-_____________________________________________
# ______________________________________________________________________________
# ______________________________________________________________________________


class YahooScrape():
    '''
    '''

    def __init__(self):
        '''
        '''
        self.STB = ScrapeToolbelt()
        self.url_contests = '''https://dfyql-ro.sports.yahoo.com/v2/contestsFilteredWeb?lang=en-US&region=US&device=desktop&sport=mlb&entryFeeMin=0&entryFeeMax=2625&sortAsc=false&slateTypes=SINGLE_GAME&slateTypes=MULTI_GAME'''
        self.date_today = datetime.today().strftime('%Y-%m-%d')

# ------------------------------------------------------------------------------
# ..................Initial Create of Master Dictionary.........................

    def create_dir(self):
        '''
        '''
        try:
            os.mkdir(f'C:/Users/okiem/github/mlb-dfs/data/{self.date_today}')
        except FileExistsError:
            pass

# ------------------------------------------------------------------------------

    def create_contests_dct(self):
        '''
        '''
        self.dct_master = self.STB.get_json(self.url_contests)
        logger_info.info('in initial -------> COMPLETED: created_contests_dct()')

        return self.dct_master
# ------------------------------------------------------------------------------

    def insert_master_dct(self):
        '''
        '''
        self.STB.dump_json(self.dct_master, filename='master')
        logger_info.info('in initial -------> COMPLETED: insert_master_dct()')

    def get_contest_times(self):
        '''
        '''
        dct = self.STB.open_json(filename='master')
        set_times = {datetime.fromtimestamp(int(t.get('startTime')/1000)).strftime('%H:%M')
                     for t in dct.get('contests').get('result')}
        if set_times:
            logger_info.info('in initial -------> SUCCESS: get_contest_times()')
        else:
            logger_error.info('in initial -------> WARNING: get_contest_times(), the contest times set is empty.')

        return set_times

    def create_scheduled_task(self):
        '''
        '''
        schtasks = r'C:\Windows\System32\schtasks.exe'
        command = r'C:\Users\okiem\github\mlb-dfs\batch\run_final_update.bat'
        set_times = self.get_contest_times()
        # Clear contents of file
        open('C:/Users/okiem/github/mlb-dfs/batch/final_update_tasks.bat', 'w').close()
        # Write new commands based on contest times
        for i in range(0, len(set_times)):
            f = open('C:/Users/okiem/github/mlb-dfs/batch/final_update_tasks.bat', 'a')
            f.write('\n')
            f.write(f'{schtasks} /create /tn YS-run_final_update{i} /sc daily /st {set_times.pop()} /tr {command} /f')
            f.close()
        logger_info.info('in initial -------> SUCCESS: create_scheduled_task()')

# ------------------------------------------------------------------------------
# ---------------Update Master Dictionary--------------------------------------

    def get_recent_contests(self):
        '''
        '''
        self.dct_update = self.STB.get_json(self.url_contests)
        if self.dct_update:
            logger_info.info('in update --------> SUCCESS: self.dct_update created')
        else:
            logger_error.warning(f'in update --------> WARNING: self.dct_update is Empty. Investigate: get_json(), {self.url_contests}')

        self.dct_master = self.STB.open_json(filename='master')
        if self.dct_master:
            logger_info.info('in update --------> SUCCESS: self.dct_master created')
        else:
            logger_error.warning(f'in update --------> WARNING: self.dct_master is Empty. Investigate: get_json(), {self.url_contests}')

        return self.dct_update
# ------------------------------------------------------------------------------

    def compare_contests(self):
        '''
        '''
        lst_master_contests = self.STB.create_lst(dct=self.dct_master, key='id')
        lst_recent_contests = self.STB.create_lst(dct=self.dct_update, key='id')
        logger_info.info(f'''in update --------> SUCCESS: lst_master_contests({len(lst_master_contests)}), lst_recent_contests created({len(lst_recent_contests)})''')

        if lst_master_contests == lst_recent_contests:
            logger_info.info('''in update --------> STOPPED: compare_contests() ... lst_master_contests == lst_recent_contests''')
        else:
            logger_info.info('in update --------> CONTINUE: compare_contests() ... lst_master_contests /= lst_recent_contests')
            try:
                self.lst_update = list(set(lst_master_contests).symmetric_difference(set(lst_recent_contests)))
                if self.lst_update:
                    for index, contest in enumerate(self.dct_master.get('contests').get('result')):
                        if contest.get('id') in self.lst_update:
                            self.lst_update.remove(contest.get('id'))
                logger_info.info('in update --------> SUCCESS: lst_update creation complete')
            except:
                logger_error.exception('in update --------> FAILED: lst_update failed to be created')

# ------------------------------------------------------------------------------

    def update_master_dct(self):
        '''
        '''
        if self.lst_update:
            for index, contest in enumerate(self.dct_update.get('contests').get('result')):
                if contest.get('id') in self.lst_update:
                    self.dct_master.get('contests').get('result').append(self.dct_update.get('contests').get('result')[index])
            self.STB.dump_json(self.dct_master, filename='master')
            logger_info.info('in update --------> COMPLETED: update_master_dct()')
        else:
            logger_info.info('in update --------> COMPLETED: update_master_dct() ... No new contests in dct_update, only expired contests in dct_master')

# ------------------------------------------------------------------------------
# ---------------Final Update Of Master Dictionary------------------------------

    def create_contestid_lst(self, date=datetime.today().strftime('%Y-%m-%d')):
        '''
        '''
        self.dct_master = self.STB.open_json(filename='master', date=date)
        self.lst_contestid = self.STB.create_lst(dct=self.dct_master, key='id')
        logger_info.info('in final_update --------> COMPLETED: create_contestid_lst()')

# ------------------------------------------------------------------------------

    def create_entryid_lst(self):
        '''
        '''
        for index, contestid in enumerate(self.lst_contestid):
            lst_entryid = []
            url = f'https://dfyql-ro.sports.yahoo.com/v2/contestEntries?lang=en-US&region=US&device=desktop&sort=rank&contestId={contestid}&start=0&limit=50'
            total_entries = self.STB.get_json(url).get('pagination').get('result').get('totalCount')
            lst_interval = list(range(0, total_entries, 50))
            for index2, start in enumerate(lst_interval):
                url = f'https://dfyql-ro.sports.yahoo.com/v2/contestEntries?lang=en-US&region=US&device=desktop&sort=rank&contestId={contestid}&start={start}&limit=50'
                data_json = self.STB.get_json(url)
                try:
                    for i in range(0, 50):
                        lst_entryid.append(data_json.get('entries').get('result')[i].get('id'))
                except IndexError:
                    pass
                except:
                    logger_error.exception('in final_update --------> Something went wrong when creting entryid list')

            self.dct_master.get('contests').get('result')[index]['EntryIDs'] = list(OrderedDict.fromkeys(lst_entryid))

        self.STB.dump_json(self.dct_master, filename='master')
        logger_info.info('in final_update --------> COMPLETED: create_entryid_lst()')
# ------------------------------------------------------------------------------

    def get_entry_rosters(self):
        '''
        '''
        self.dct_master = self.STB.open_json(filename='master', date='2021-05-23')
        for index, contest in enumerate(self.dct_master.get('contests').get('result')):
            print(index)
            self.dct_master.get('contests').get('result')[index]['EntryRosters'] = []
            for index2, entryid in enumerate(self.dct_master.get('contests').get('result')[index].get('EntryIDs')):
                url = f'https://dfyql-ro.sports.yahoo.com/v2/contestEntry/{entryid}?lang=en-US&region=US&device=desktop&slateTypes=SINGLE_GAME&slateTypes=MULTI_GAME'
                data_json = self.STB.get_json(url)
                self.dct_master.get('contests').get('result')[index]['EntryRosters'].append(data_json)
                print('*')
                

        #logger_info.info('in final_update --------> COMPLETED: get_entry_rosters()')
# ______________________________________________________________________________


class MKFScrape():
    '''
    '''

    def __init__(self):
        '''
        '''
        self.STB = ScrapeToolbelt()
        

# ______________________________________________________________________________


class FangraphsScrape():
    '''
    '''

    def __init__(self):
        '''
        '''
        self.STB = ScrapeToolbelt()
