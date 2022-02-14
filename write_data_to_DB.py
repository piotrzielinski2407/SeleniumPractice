from pandas_columns_name import pandas_teams_columns_name
from cache import cache_history
from sql_postgress_comms import DB
from logger import logger_object

class SaveScrappedData(DB):
    def __init__(self, df_matches, df_players_stats, df_players_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df_matches = df_matches
        self.df_players_stats = df_players_stats
        self.df_players_info = df_players_info
        self.df_teams = self.__prepare_teams_df()
        self.__prepare_players_stats()

    def save_data(self):
        self.__save_teams()
        self.__save_matches()
        self.__save_player_info()
        self.__save_player_stats()

    def __save_teams(self):
        _table_name = 'teams'
        logger_object.log('Save teams triggeregd', 'DEBUG')
        self.insert_data(self.df_teams, table_name = _table_name)

    def __save_matches(self):
        if len(self.df_matches) > 0:
            _table_name = 'matches'
            logger_object.log('Save matches triggeregd', 'DEBUG')
            self.insert_data(self.df_matches, table_name = _table_name)
        else:
            logger_object.log('No matches to save', 'DEBUG')

    def __save_player_info(self):
        if len(self.df_players_info) > 0:
            _table_name = 'players_info'
            logger_object.log('Save players info triggeregd', 'DEBUG')
            self.insert_data(self.df_players_info, table_name = _table_name)
        else:
            logger_object.log('No players info to save', 'DEBUG')
        
    def __save_player_stats(self):
        if len(self.df_players_stats) > 0:
            _table_name = 'players_statistic'
            logger_object.log('Save players stats triggeregd', 'DEBUG')
            self.insert_data(self.df_players_stats, table_name = _table_name)
        else:
            logger_object.log('No players stats to save', 'DEBUG')

    def __prepare_players_stats(self):
        self.df_players_stats.drop('player_hyperlink', inplace = True, axis = 1)

    def __prepare_teams_df(self):
        '''
        Function that will convert dataframe from matches scraping to teams, 
        warning: direct connection to columns names from pands_columns_name file
        '''
        #need to add verification what teams are already in DB
        league_full_name = cache_history.load_league_full_name()
        teams_ids_in_DB = cache_history.load_teams_ids()
        df1 = self.df_matches[['league_ticker','id_flashscore_home_team', 'home_team', 'home_team_ticker']].drop_duplicates(subset='id_flashscore_home_team')
        df2 = self.df_matches[['league_ticker','id_flashscore_away_team','away_team', 'away_team_ticker']].drop_duplicates(subset='id_flashscore_away_team')

        df1['temp'] = league_full_name
        df2['temp'] = league_full_name

        df1 = df1[['temp', 'league_ticker','id_flashscore_home_team', 'home_team', 'home_team_ticker']]
        df2 = df2[['temp', 'league_ticker','id_flashscore_away_team', 'away_team', 'away_team_ticker']]

        df1.columns = pandas_teams_columns_name
        df2.columns = pandas_teams_columns_name

        df1 = df1.append(df2, ignore_index=True)
        df1 = df1.drop_duplicates(subset='id_flashscore_team')
        df1 = df1[~df1['id_flashscore_team'].isin(teams_ids_in_DB)]
        return df1

