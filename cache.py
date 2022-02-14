from singleton import Singleton
from sql_postgress_comms import DB
from settings import load_settings
from sql_postgress_comms import DB

class CacheHistory(DB, metaclass = Singleton):
    
    def __init__(self,  *args, **kwargs):
        '''
        Class to cache results from DB to avoid scrapping information already scrapped before
        '''
        super().__init__( *args, **kwargs)
        
        self.league = load_settings()['league_ticker']
    
    def load_teams_ids(self):
        table_name = 'teams'
        return_column_name = "id_flashscore_team"
        result = self.return_data(table_name=table_name, columns_to_return=return_column_name)
        return result

    def load_match_ids(self):
        table_name = 'matches'
        return_column_name = "id_flashscore_match"
        condition_column_name = "league_ticker"
        result = self.return_data(table_name=table_name, columns_to_return=return_column_name,
                     condition_column = condition_column_name, condition_argument = self.league)
        return result

    def load_player_ids(self):
        table_name = 'players_info'
        return_column_name = "id_flashscore_player"
        result = self.return_data(table_name=table_name, columns_to_return=return_column_name)
        return result

    def load_league_full_name(self):
        table_name = 'leagues'
        return_column_name = "league_full_name"
        condition_column_name = "league_ticker"
        result = self.return_data(table_name=table_name, columns_to_return=return_column_name,
                     condition_column = condition_column_name, condition_argument = self.league)
        try:
            return result[0]
        except:
            return None

    def load_league_prefix(self):
        table_name = 'leagues'
        return_column_name = "league_hyperlink_prefix"
        condition_column_name = "league_ticker"
        result = self.return_data(table_name=table_name, columns_to_return=return_column_name,
                     condition_column = condition_column_name, condition_argument = self.league)
        try:
            return result[0]
        except:
            return None

    def close_DB_interface(self):
        self.close_cur()
        self.close_conn()


cache_history = CacheHistory()


if __name__ == '__main__':
    #some testing here
    cache_history.league = 'ACB'
    print(cache_history.load_match_ids())
    

  
 
    

   