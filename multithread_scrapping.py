#from threading_lock import data_lock
from statistics_scraper import MatchScrapper
from logger import logger_object
from settings import load_settings
import threading
import pandas as pd
from pandas_columns_name import pandas_matches_columns_names, pandas_players_stats_columns_names

data_lock = threading.Lock()
global_settings = load_settings()
no_of_threads = int(global_settings['no_of_threads'])

class MatchScrapClientHandler():
    '''
    Class to control all threads and buffer all results form threads
    '''
    def __init__(self, ids_to_scrap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_handler = idToScrapHandler(ids_to_scrap)
        self.df_matches_columns = pandas_matches_columns_names
        self.df_players_stats_columns = pandas_players_stats_columns_names        
        self.matches_stats = []
        self.players_stats = []
        self.threads = []
        self.no_of_threads = no_of_threads

    def get_matches_data(self):
        try:
            return pd.DataFrame(self.matches_stats,columns = self.df_matches_columns)
        except:
            return self.matches_stats

    def get_players_data(self):
        try:
            return pd.DataFrame(self.players_stats,columns = self.df_players_stats_columns)
        except:
            return self.players_stats

    def create_threads(self):
        logger_object.log("Create threads activated", 'DEBUG')
        for i in range(self.no_of_threads):
            thread = MatchScrapClient(self.id_handler, self.matches_stats, 
                                        self.players_stats, i)
            self.threads.append(thread)
            logger_object.log(f"Thread no: {i} created", 'DEBUG')
            thread.start()
        
        for thread in self.threads:
            thread.join()

    

class MatchScrapClient(threading.Thread):
    '''
    Single thread for scrapping
    '''
    def __init__(self, id_handler, match_data, player_stats_data, thread_no, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrapper = MatchScrapper()
        self.id_handler = id_handler
        self.match_data = match_data
        self.player_stats_data = player_stats_data
        self.thread_no = thread_no

    def run(self):
        while True:
            logger_object.log(f"Thread {self.thread_no} started", 'DEBUG')
            data_lock.acquire()
            id_to_process = self.id_handler.retrive_id()
            data_lock.release()

            if id_to_process == None:
                logger_object.log(f"Thread no {self.thread_no} ended all tasks", 'DEBUG')
                break

            self.scrapper.id = id_to_process
            self.scrapper.scrap_it()
            data_lock.acquire()
            self.save_match_data(self.scrapper.match_summary_list)
            self.save_player_stats_data(self.scrapper.players_stats)
            data_lock.release()

    def save_match_data(self, _match_data):
        #tu trzeba poprawić bo się wydłuża lista a nie dodają nowe listy
        if len(_match_data)>0:
            self.match_data.append(_match_data)

    def save_player_stats_data(self, _player_stats_data):
        result = _player_stats_data
        for row in result:
            self.player_stats_data.append(row) 
    
class idToScrapHandler():
    def __init__(self, ids_to_scrap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids_to_scrap = ids_to_scrap

    @property
    def ids_to_scrap(self):
        return self._ids_to_scrap

    @ids_to_scrap.setter
    def ids_to_scrap(self, new_value):
        if isinstance(new_value, list):
            self._ids_to_scrap = new_value.copy()
            logger_object.log("Id's loading to handler sucess!", 'DEBUG')

    def retrive_id(self):
        if len(self.ids_to_scrap) != 0 :
            id_to_return = self.ids_to_scrap.pop()
        else:
            id_to_return = None
        logger_object.log(f"ID = {id_to_return} pop up from id's list", 'DEBUG')
        return id_to_return   



if __name__ == '__main__':
    id_s = ['OdMeLm89', 'OOdFExif', 'pARqJX0T']
    no_of_threads = 3
    handler = MatchScrapClientHandler(id_s)
    handler.create_threads()
    print(handler.get_matches_data())
    print(handler.get_players_data())




