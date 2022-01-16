from webpageprep import PreparePageSource
from threading_lock import data_lock
from hyperlinks_handler import MatchLinkCreator
from logger import logger_object
from settings import load_settings
from datetime import datetime

global_settings = load_settings()


class MatchScrapper(PreparePageSource, MatchLinkCreator):
    date_time_div_name = 'duelParticipant__startTime'
    team_div_names = ['smh__participantName smh__home', 'smh__participantName smh__away']
    points_div_names = ['smh__part smh__home smh__part--1', 'smh__part smh__away smh__part--1', 'smh__part smh__home smh__part--2', 'smh__part smh__away smh__part--2', \
                        'smh__part smh__home smh__part--3', 'smh__part smh__away smh__part--3',  'smh__part smh__home smh__part--4', 'smh__part smh__away smh__part--4', \
                        'smh__part smh__home smh__part--5', 'smh__part smh__away smh__part--5']
    odds_cell_selector = 'oddsCell__odd'
    player_row_selector = 'ui-table__row playerStatsTable__row'
    player_hyperlink_selector = 'playerStatsTable__cell playerStatsTable__participantCell playerStatsTable__cell--clickable playerStatsTable__cell--shadow'
    player_name_selector = 'playerStatsTable__participantNameCell'
    player_team_ticker_selector = 'playerStatsTable__cell playerStatsTable__teamCell'
    player_points_selector = 'playerStatsTable__cell playerStatsTable__cell--sortingColumn'
    player_stats_selector = 'playerStatsTable__cell'

    def __init__(self,  *args, id = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.match_summary_link = None
        self.player_summary_link = None
        self.odds_summary_link = None
        self.id = id
        self.date_lower_limit = datetime.strptime(global_settings['start_date'],"%Y.%m.%d")
        self.date_upper_limit = datetime.strptime(global_settings['end_date'],"%Y.%m.%d")
        self.league = global_settings['league_ticker']
        self.match_summary_list = []
        self.home_odds = []
        self.away_odds = []
        self.players_stats = []
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value):
        if new_value is not None:
            self._id = new_value
            self.match_summary_link = self.create_match_summary_link()
            self.player_summary_link = self.create_player_summary_link()
            self.odds_summary_link = self.create_odds_summary_link()        

    def scrap_it(self):
        self.hyperlink = self.match_summary_link
        self.__page_content_ = self.page_content()
        if not self.__scrap_date_and_time():#if data and time scrapping was sucessful, check if date is in expected range
            #popup to next ids, clear self data
            logger_object.log(f'Unable to extract date and time from: "{self.hyperlink}", scraping abort', 'ERROR')
            return None

        if not (self.date < self.date_upper_limit and self.date > self.date_lower_limit):
            #popup to next ids, clear self data
            logger_object.log(f'Match from: "{self.hyperlink}" beyond selected data, scraping abort', 'INFO')
            return None
        #match statistic scrapping
        self.match_summary_list.append(self.id)
        self.match_summary_list.append(self.league)
        self.match_summary_list.append(self.date.strftime("%Y.%m.%d"))
        self.match_summary_list.append(self.time.strftime("%H:%M"))
        self.__scrap_team_names()
        self.match_summary_list.append(self.hyperlink)
        self.__scrap_points()
        #odds scrapping section start here
        self.hyperlink = self.odds_summary_link
        self.__page_content_ = self.page_content()
        self.__scrap_odds()
        #player statistic scrapping
        self.hyperlink = self.player_summary_link
        self.__page_content_ = self.page_content()
        self.__scrap_players_complete_info()

    def __scrap_players_complete_info(self):
        rows = self.__extract_all_classes(MatchScrapper.player_row_selector)

        for row in rows:
            row_data = []
            row_data.append(self.id)
            row_data.append(self.__scrap_player_id(row))
            row_data.append(self.__scrap_player_name(row))
            row_data.append(self.__scrap_player_team_ticker(row))
            row_data.append(self.__scrap_player_points(row))
            player_game_stats = self.__scrap_player_stats(row)
            row_data = row_data + player_game_stats
            
            self.players_stats.append(row_data)
            
        
    def __scrap_player_id(self, row):
        href_raw = row.find('a', class_ =  MatchScrapper.player_hyperlink_selector)
        href = href_raw.get('href')
        return href[href[:-1].rfind('/')+1:-1]

    def __scrap_player_name(self, row):
        name = self.__extract_text_from_selector('div', MatchScrapper.player_name_selector,page_content = row)
        return name

    def __scrap_player_team_ticker(self, row):
        team_ticker = self.__extract_text_from_selector('div', MatchScrapper.player_team_ticker_selector,page_content = row)
        return team_ticker
    
    def __scrap_player_points(self, row):
        player_points = self.__extract_text_from_selector('div', MatchScrapper.player_points_selector,page_content = row)
        return player_points

    def __scrap_player_stats(self, row):
        player_stats = self.__extract_text_from_all_selectors('div', MatchScrapper.player_stats_selector,  page_content = row)
        return player_stats

    def __scrap_odds(self):
        def divide_odd(odds_list):
            result=[]
            for odd_raw in odds_list:
                
                divider = odd_raw.find("»")
                if divider != -1:
                    result.append(odd_raw[:divider-1].strip())
                    result.append(odd_raw[divider+1:].strip())
                else:
                    odd = odd_raw.strip()
                    result.append(odd)
                    result.append(odd)#double append on purpouse to match sizes in case odd od not change
            return result

        self.hyperlink = self.odds_summary_link
        self.__page_content_ = self.page_content()

        odds_classes = self.__extract_all_classes(MatchScrapper.odds_cell_selector)
        odds_raw = []

        try:
            for odd_cell in odds_classes:
                    raw_text = str(odd_cell.get('title'))
                    if raw_text == '':
                        raw_text = str(odd_cell.getText())
                    odds_raw.append( raw_text.replace('Odds removed by bookmaker.','').strip() )

            home_odds_raw = odds_raw[::2]
            away_odds_raw = odds_raw[1::2]
            self.home_odds = divide_odd(home_odds_raw)
            self.away_odds = divide_odd(away_odds_raw)
            self.match_summary_list.append(','.join(self.home_odds[::2]))
            self.match_summary_list.append(','.join(self.away_odds[::2]))
            self.match_summary_list.append(','.join(self.home_odds[1::2]))
            self.match_summary_list.append(','.join(self.away_odds[1::2]))

        except Exception as e:
            logger_object.log(f'Exception {e} occured', 'ERROR')

    def __scrap_points(self):
        for div_name in MatchScrapper.points_div_names:
            points = self.__extract_text_from_selector('div', div_name)
            if points != ('' or None):
                self.match_summary_list.append(points)
            else:
                self.match_summary_list.append('0')

    def __scrap_team_names(self):
        result = [self.__extract_text_from_selector('div', div_name) for div_name in MatchScrapper.team_div_names]
        self.match_summary_list.append(result[0])
        self.match_summary_list.append(result[1])

    def __scrap_date_and_time(self):
        extracted_text = self.__extract_text_from_selector('div', MatchScrapper.date_time_div_name)
        if extracted_text is not None:
            self.date = datetime.strptime(extracted_text[0:10],"%d.%m.%Y")
            self.time = datetime.strptime(extracted_text[11:16],"%H:%M")
            return True
        else:
            return False

    def __extract_text_from_selector(self, selector, div_name, skip_null_values = True, page_content = None):
        '''
        Method that will extract text from choosen selector and selector_name by default whole page content
        is using, but can be provided by variable page_content
        '''
        
        if page_content == None:
            raw_text = self.__page_content_.find(selector, class_ = div_name)
        else:
            raw_text = page_content.find(selector, class_ = div_name)
        
        if raw_text is not None:
            processed_text = (raw_text.getText()).strip()
        
            if processed_text != '' or not skip_null_values:
                return processed_text
        logger_object.log(f'Text in {selector}: "{div_name}" from: "{self.hyperlink}" not found', 'ERROR')
        return None

    def __extract_all_classes(self, class_name):
        extracted_clases = self.__page_content_.findAll(class_ = class_name)
        if extracted_clases is not None:
            return extracted_clases
        logger_object.log(f'Unable to find class: "{class_name}" in: "{self.hyperlink}"', 'ERROR')
        return None

    def __extract_text_from_all_selectors(self, selector, div_name,  page_content = None, precise_match = True):
        '''
        Method that will extract text from all choosen selectors and selector_name by default whole page content
        is using, but can be provided by variable page_content, results retured as list, empty elements returned as empty string
        '''

        if page_content == None:
            page_content=self.__page_content_

        if precise_match:
            lines = page_content.findAll(lambda tag: tag.name == selector and tag.get('class') == [div_name])
        else:
            lines = page_content.findAll(selector, class_ = div_name)

        results = []
        for line in lines:
            text = str(line.getText()).strip()
            if text == None:
                text = ''
            results.append(text)
        return results

if __name__ == '__main__':
    test = MatchScrapper(id = 'GhOXKjn8')
    test.scrap_it()
    print(test.match_summary_list)
    print(test.players_stats)