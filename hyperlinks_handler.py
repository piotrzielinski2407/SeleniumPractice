from settings import load_settings
from aditional_functions import DateHandler
from logger import logger_object
from exceptions import *
from aditional_functions import substract_list_content
from cache import cache_history


class ArchiveLinkCreator(DateHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__global_stettings = load_settings()
        self.__league_ticker = self.__global_stettings['league_ticker']
        self.__hyperlink_prefix = cache_history.load_league_prefix()

        if self.__hyperlink_prefix is not None:
            self.__start_year = DateHandler(date = self.__global_stettings['start_date']).year
            self.__end_year = DateHandler(date = self.__global_stettings['end_date']).year
            self.__year_span = self.__year_span_calculation()
            self.__hyperlinks = self.__create_hyperlinks()
        else:
            logger_object.log('No links created, prefix missing', 'ERROR')
            self.__hyperlinks = None

    def return_hyperlinks(self):
        return self.__hyperlinks


    def __create_hyperlinks(self):
        year1 =  self.__start_year - 1
        year2 = self.__start_year
        hyperlinks = []
        for _ in range(self.__year_span):
            hyperlinks.append(self.__hyperlink_prefix + f'{year1}-{year2}/results/')
            year1+=1
            year2+=1
        return hyperlinks

    def __year_span_calculation(self):
        year_span = self.__end_year - self.__start_year
        if year_span < 0:
            logger_object.log('Start date is later than end date', 'ERROR')
            raise WrongDateException
        return int(year_span)+2 #is nescessary to add 2 to cover seasons that took in half of selected year, because each season is played during winter so year timestamp will change by
    
    def __str__(self):
        return 'Creator links to archives of seasons'

    def __repr__(self):
        return 'ArchiveLinkCreator()'

class MatchLinkCreator():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None
        self.hyperlink_prefix = 'https://www.flashscore.com/match/'

    def create_match_summary_link(self):
        suffix = '/#match-summary/match-summary'
        result = self.__link_joiner(suffix)
        logger_object.log(f'{len(result)} match summary link created', 'INFO')
        return result

    def create_player_summary_link(self):#outdated, unused function
        suffix = '/#match-summary/player-statistics/0'
        result = self.__link_joiner(suffix)
        logger_object.log(f'{len(result)} players statistic link created', 'INFO')
        return result

    def create_player_summary_link_home_team(self):
        suffix = '/#match-summary/player-statistics/1'
        result = self.__link_joiner(suffix)
        logger_object.log(f'{len(result)} players statistic from home team link created', 'INFO')
        return result

    def create_player_summary_link_away_team(self):
        suffix = '/#match-summary/player-statistics/2'
        result = self.__link_joiner(suffix)
        logger_object.log(f'{len(result)} players statistic from away team link created', 'INFO')
        return result

    def create_odds_summary_link(self):
        suffix = '/#odds-comparison/home-away/ft-including-ot'
        result = self.__link_joiner(suffix)
        logger_object.log(f'{len(result)} odds statistic link created', 'INFO')
        return result

    def __link_joiner(self, suffix):
        if self.id is not None:
            prefix = self.hyperlink_prefix
            link = prefix + self.id + suffix 
            return link
        logger_object.log('Id not set unable to create hyperlink', 'ERROR')

def players_links_to_scrap(df_players_stats):
    df_players_stats_trimmed = df_players_stats.drop_duplicates(subset = 'id_flashscore_player', inplace=False)[['id_flashscore_player', 'player_hyperlink']]
    players_id_in_DB = cache_history.load_player_ids()
    scrapped_players_ids = df_players_stats_trimmed['id_flashscore_player'].tolist()
    if len(players_id_in_DB) != 0:
        players_id_to_scrap = substract_list_content(scrapped_players_ids,players_id_in_DB)
    else:
        players_id_to_scrap = scrapped_players_ids
    hyperlinks = df_players_stats_trimmed[df_players_stats_trimmed['id_flashscore_player'].isin(players_id_to_scrap)]['player_hyperlink'].tolist()
    return hyperlinks

if __name__ == '__main__':
    #some testing here  
    settings = load_settings()

    
    test = ArchiveLinkCreator()
    print(test.return_hyperlinks())