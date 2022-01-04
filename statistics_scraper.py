from re import S
from webpageprep import PreparePageSource
from threading_lock import data_lock
from hyperlinks_handler import MatchLinkCreator
from logger import logger_object
from settings import load_settings
from datetime import datetime

global_settings = load_settings()

class StatisticScrapper(PreparePageSource, MatchLinkCreator):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.match_summary_link = None
        self.player_summary_link = None
        self.odds_summary_link = None

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



class MatchSummaryScrapper(PreparePageSource):
    date_time_div_name = 'duelParticipant__startTime'
    team_div_names = ['smh__participantName smh__home', 'smh__participantName smh__away']
    points_div_names = ['smh__part smh__home smh__part--1', 'smh__part smh__away smh__part--1', 'smh__part smh__home smh__part--2', 'smh__part smh__away smh__part--2', \
                        'smh__part smh__home smh__part--3', 'smh__part smh__away smh__part--3',  'smh__part smh__home smh__part--4', 'smh__part smh__away smh__part--4', \
                        'smh__part smh__home smh__part--5', 'smh__part smh__away smh__part--5']

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_lower_limit = datetime.strptime(global_settings['start_date'],"%Y.%m.%d")
        self.date_upper_limit = datetime.strptime(global_settings['end_date'],"%Y.%m.%d")
        self.return_list = []#started with date, flasscore id and league ticker should be added in child class
        

    def scrap_it(self, hyperlink):
        self.hyperlink = hyperlink
        self.__page_content_ = self.page_content()
        if not self.__scrap_date_and_time():#if data and time scrapping was sucessful, check if date is in expected range
            #popup to next ids, clear self data
            logger_object.log(f'Unable to extract date and time from: "{self.hyperlink}", scraping abort', 'ERROR')
            return None

        if not (self.date < self.date_upper_limit and self.date > self.date_lower_limit):
            #popup to next ids, clear self data
            logger_object.log(f'Match from: "{self.hyperlink}" beyond selected data, scraping abort', 'INFO')
            return None
        
        self.return_list.append(self.date)
        self.return_list.append(self.time)
        self.return_list + self.__scrap_team_names()
        self.return_list.append(self.hyperlink)
        self.__scrap_points()
        #ended here (now odd scraping)

    def __scrap_points(self):
        for div_name in MatchSummaryScrapper.points_div_names:
            points = self.__extract_text_from_div(div_name)
            if points != '':
                self.return_list.append(points)
            else:
                self.return_list.append('0')

    def __scrap_team_names(self):
        result = [self.__extract_text_from_div(div_name) for div_name in MatchSummaryScrapper.team_div_names]
        return result

    def __scrap_date_and_time(self):
        extracted_text = self.__extract_text_from_div(MatchSummaryScrapper.date_time_div_name)
        if extracted_text is not None:
            self.date = datetime.strptime(extracted_text[0:10],"%d.%m.%Y")
            self.time = datetime.strptime(extracted_text[11:16],"%H:%M")
            return True
        else:
            return False

    def __extract_text_from_div(self, div_name, skip_null_values = True):
        raw_text = self.__page_content_.find('div', class_ = div_name)
        if raw_text is not None:
            processed_text = (raw_text.getText()).strip()
        
            if processed_text != '' or not skip_null_values:
                return processed_text
        logger_object.log(f'Text in div: "{div_name}" from: "{self.hyperlink}" not found', 'ERROR')
        return None




if __name__ == '__main__':
    test = MatchSummaryScrapper()
    print(test.date_upper_limit)
    print(test.date_lower_limit)