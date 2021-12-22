from settings import load_hyperlink_settings, load_settings
from aditional_functions import DateHandler
from logger import logger_object
from exceptions import *


class ArchiveLinkCreator(DateHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__global_stettings = load_settings()
        self.__league_ticker = self.__global_stettings['league_ticker']
        self.__class_settings = load_hyperlink_settings()
        self.__hyperlink_prefix = self.__class_settings[self.__league_ticker]
        self.__start_year = DateHandler(date = self.__global_stettings['start_date']).year
        self.__end_year = DateHandler(date = self.__global_stettings['end_date']).year
        self.__year_span = self.__year_span_calculation()
        self.__hyperlinks = self.__create_hyperlinks()

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




if __name__ == '__main__':
    #some testing here  

    test = ArchiveLinkCreator()
    print(test.hyperlinks)