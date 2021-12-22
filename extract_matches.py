from webpageprep import *
from logger import logger_object

class ExtractMatchIds(PreparePageSource):
    '''
    Class to extract match id's based on provided link to archive season.
    '''
    __match_containers_name = ['event__match event__match--static event__match--twoLine',
                              'event__match event__match--static event__match--last event__match--twoLine']
    __general_container_list = 'container'
    __show_more_matches_text = 'Show more matches'
    __id_prefix = 'g_3_'
    
    def __init__(self, hyperlinks = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__match_id = []
        self.hyperlink = None
        self.hyperlinks = hyperlinks    

    @property
    def hyperlinks(self):
        return self._hyperlinks

    @hyperlinks.setter
    def hyperlinks(self, new_value):
        self._hyperlinks = new_value
        if new_value:
            self.__scrap_all_hyperlinks()
    
    def __scrap_all_hyperlinks(self):
        for hyperlink in self.hyperlinks:
            self.hyperlink = hyperlink
            self.__load_all_matches()
            self.get_matches_id()

    def __load_all_matches(self):
        #some exceptions may be raised here, due to time nescessary for page to load all elements
        xpath_command = "//*[text() = '" + str(ExtractMatchIds.__show_more_matches_text) + "']"
        elements = self.driver.find_elements_by_xpath(xpath_command)
        
        while True:
            self.wait_for_page_to_load()
            self.driver.implicitly_wait(self.page_load_treshold)
            for element in elements:
                try:
                    self.driver.execute_script("arguments[0].click()", element)
                except Exception as e:
                    logger_object.log(f'Exception occured: {e}', 'WARNING')
                    pass
            try:
                if not self.__is_string_on_site():
                    logger_object.log('All matches loaded', 'INFO')
                    break
            except Exception as e:
                logger_object.log(f'Exception occured: {e}. Script suspended and wait for all elements load',
                         'WARNING')
                time.sleep(0.25)
    
    def return_matches_id(self):
        self.get_matches_id()
        return self.__match_id

    def get_matches_id(self):
        self.__match_id = []
        self.__scrap_by_container(self.page_content())

    def __scrap_by_container(self, page_content):
        for container in ExtractMatchIds.__match_containers_name:

            matches = page_content.find_all('div', class_ = container)
            self.__match_id = self.__match_id + [self.__extract_id(match) for match in matches]

    def __extract_id(self, soup_row):
        return str(soup_row.get('id')).replace(ExtractMatchIds.__id_prefix,'')
    
    def __is_string_on_site(self):
        temp = self.driver.find_element_by_class_name(ExtractMatchIds.__general_container_list).text
        temp = temp.find(ExtractMatchIds.__show_more_matches_text)
        if temp == -1:
            return False
        return True

    def __repr__(self):
        return f'ExtractMatchIds({self.hyperlink})'

    def __str__(self):
        return f'Prepared match ids from hyperlink: {self.hyperlink}'