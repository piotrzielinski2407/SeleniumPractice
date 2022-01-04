from singleton import Singleton
from threading_lock import data_lock
from sql_postgress_comms import DB
from exceptions import QuerryException
from settings import load_settings

class CacheHistory(DB, metaclass = Singleton):
    
    def __init__(self,  *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.history = {}
        self.league = load_settings()['league_ticker']
        

    def team_ticker_load(self):
        table_name = 'leagues'
        return_column_name = "league_hyperlink"
        condition_column_name = "league_ticker"
        result = self.__querry_with_condition_equal(table_name, return_column_name,
                                                    condition_column_name, self.league)
        self.history[self.league + '_hyperlink'] = result[0]

    def load_match_ids(self):
        table_name = 'Matches'
        return_column_name = "id_flashscore_match"
        condition_column_name = "league_ticker"
        result = self.__querry_with_condition_equal(table_name, return_column_name,
                                            condition_column_name, self.league)
        return result

    def __querry_with_condition_equal(self, table_name, return_column_name,
                                condition_column_name, condition):
        sql = f"SELECT {return_column_name }\
        FROM {table_name}\
        WHERE {condition_column_name} = '{condition}';"
        result = self.execute(sql)
        if result is not False:
            result = self.fetchall()
            return result
        else:
            raise QuerryException('Error during querry sql command')

cache_history = CacheHistory()

def cache(method):
    def wrapper(self, x):
        data_lock.acquire()
        if x not in cache_history.history:
            cache_history.history[x] = method(self, x)
            print('saved in cache')
        print('return from cache')
        data_lock.release()
        return cache_history.history[x] 
    return wrapper


if __name__ == '__main__':
    #some testing here
    
    
    cache_history.team_ticker_load()

    cache_history.load_match_ids()
    
    'UypWUgbG1' in cache_history.history
  
    '''
    db = DB()
    
    table_name = 'teams'
    data = [
            ['Liga Endesa', 'ACB', 'Baskonia', 'BAS'],
            ['Liga Endesa', 'ACB', 'Fuenlabrada', 'FUE']
            ]
    db.insert_data(data, table_name = table_name)
    
    table_name = 'matches'
    data = [
            ['UypWUgbG', 'ACB', '2019.04.28', '19:30', 'BAS', 'FUE', 'https://www.flashscore.com/match/UypWUgbG/#match-summary/',
            '29', '20', '24', '24', '27', '29', '21', '19', '0', '0', '1.05', '6.90', '1.05', '8.30']
            ]
    db.insert_data(data, table_name = table_name)
    '''
 
    

   