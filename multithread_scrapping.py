#from threading_lock import data_lock
from statistics_scraper import MatchScrapper
from extract_player_info import ScrapPlayerInfo
from logger import logger_object
from settings import load_settings
import threading
import pandas as pd
from pandas_columns_name import pandas_matches_columns_names, pandas_players_stats_columns_names,pandas_players_info_columns_names

data_lock = threading.Lock()
global_settings = load_settings()
no_of_threads = int(global_settings['no_of_threads'])

#MATCH STATISTICS SCRAPPING
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
        for i in range(min(self.no_of_threads, len(self.id_handler.ids_to_scrap))):
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
        logger_object.log(f"Thread {self.thread_no} started", 'DEBUG')
        while True:
            data_lock.acquire()
            id_to_process = self.id_handler.retrive_id()

            if id_to_process == None: 
                logger_object.log(f"Thread no {self.thread_no} ended all tasks", 'DEBUG')
                self.scrapper.driver.quit()
                data_lock.release()
                break

            data_lock.release()
            self.scrapper.id = id_to_process
            self.scrapper.scrap_it()
            data_lock.acquire()
            self.save_match_data(self.scrapper.match_summary_list)
            self.save_player_stats_data(self.scrapper.players_stats)
            data_lock.release()

    def save_match_data(self, _match_data):
        
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


#PLAYER INFO SCRAPPING
class PlayerInfoClientHandler():
    '''
    Class that will control multithread data scrapping for player infos
    '''
    def __init__(self, hyperlinks_to_scrap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hyperlink_handler = HyperlinkToScrapHandler(hyperlinks_to_scrap)
        self.df_columns = pandas_players_info_columns_names
        self.player_info = []
        self.threads = []
        self.no_of_threads = no_of_threads

    def get_player_info(self):
        try:
            return pd.DataFrame(self.player_info, columns = self.df_columns)
        except:
            return self.player_info

    def create_threads(self):
        logger_object.log("Create threads activated", 'DEBUG')
        for i in range( min(self.no_of_threads, len(self.hyperlink_handler.hyperlinks_to_scrap) ) ):
            thread = PlayerInfoScrapClient(self.hyperlink_handler, self.player_info, i)
            self.threads.append(thread)
            logger_object.log(f"Thread no: {i} created", 'DEBUG')
            thread.start()

        for thread in self.threads:
            thread.join()
           
class PlayerInfoScrapClient(threading.Thread):
    '''
    Single thread for player info scrapping
    '''
    def __init__(self, hyperlink_handler, player_info, thread_no, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrapper = ScrapPlayerInfo()
        self.hyperlink_handler = hyperlink_handler
        self.player_info = player_info
        self.thread_no = thread_no

    def run(self):
        logger_object.log(f"Thread {self.thread_no} started", 'DEBUG')
        while True:
            data_lock.acquire()
            hyperlink_to_process = self.hyperlink_handler.retrive_hyperlink()

            if hyperlink_to_process == None:
                logger_object.log(f"Thread no {self.thread_no} ended all tasks", 'DEBUG')
                self.scrapper.driver.quit()
                data_lock.release()
                break

            data_lock.release()
            self.scrapper.hyperlink = hyperlink_to_process
            self.scrapper.scrap_it()
            data_lock.acquire()
            self.save_data(self.scrapper.return_list)
            data_lock.release()

    def save_data(self, scrapped_player_info):
        if len(scrapped_player_info) > 0:
            self.player_info.append(scrapped_player_info)

class HyperlinkToScrapHandler():
    '''
    Class to properly popup hyperlinks to thread during scrapping player info
    '''
    def __init__(self, hyperlinks_to_scrap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hyperlinks_to_scrap = hyperlinks_to_scrap

    @property
    def hyperlinks_to_scrap(self):
        return self._hyperlinks_to_scrap

    @hyperlinks_to_scrap.setter
    def hyperlinks_to_scrap(self, new_value):
        if isinstance(new_value, list):
            self._hyperlinks_to_scrap = new_value.copy()
            logger_object.log("Hyperlinks loading to handler sucess!", 'DEBUG')

    def retrive_hyperlink(self):
        if len(self.hyperlinks_to_scrap) != 0 :
            hyperlink_to_return = self.hyperlinks_to_scrap.pop()
        else:
            hyperlink_to_return = None
        logger_object.log(f"Hyperlink = {hyperlink_to_return} pop up from id's list", 'DEBUG')
        return hyperlink_to_return      

if __name__ == '__main__':
    test_list = ['https://www.flashscore.com/player/laprovittola-nicolas/ptRH5ANG/', 'https://www.flashscore.com/player/tavares-walter/rstyTK2O/',
    'https://www.flashscore.com/player/deck-gabriel/hSXwh2NS/', 'https://www.flashscore.com/player/thompkins-trey/nqUNR1zf/',
    'https://www.flashscore.com/player/llull-sergio/EyDSe5kO/']
    no_of_threads = 3
    handler = PlayerInfoClientHandler(test_list)
    handler.create_threads()
    print(handler.get_player_info())
    




