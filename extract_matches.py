from bs4 import BeautifulSoup
import pandas as pd
from webpageprep import *

class ExtractMatchIds(PreparePageSource):
    '''
    
    '''

    __external_container = 'container_div_name'
    __match_containers_name = ['event__match event__match--static event__match--twoLine',
                              'event__match event__match--static event__match--last event__match--twoLine']
    __general_container_list = 'container'
    __show_more_matches_text = 'Show more matches'
    
    def __init__(self, hyperlink, *args, **kwargs):
        super().__init__(hyperlink, *args, **kwargs)
        self.__match_id = None
        self.__load_all_matches()

    def __load_all_matches(self):
        xpath_command = "//*[text() = '" + str(ExtractMatchIds.__show_more_matches_text) + "']"
        elements = self.driver.find_elements_by_xpath(xpath_command)
        
        while True:
            self.wait_for_page_to_load()
            for element in elements:
                try:
                    self.driver.execute_script("arguments[0].click()", element)
                except:
                    pass
            try:
                if not self.__is_string_on_site():
                    break
            except:
                time.sleep(0.25)

    def __is_string_on_site(self):
        temp = self.driver.find_element_by_class_name(ExtractMatchIds.__general_container_list).text
        temp = temp.find(ExtractMatchIds.__show_more_matches_text)
        if temp == -1:
            return False
        return True