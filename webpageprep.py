from json import load
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from exceptions import *
from logger import logger_object
from settings import load_settings

global_settings = load_settings()

class PreparePageSource():
    '''
    Base class to preapre page before scrapping, might be parent to other more complex clases
    '''
    __cookie_button_name = 'onetrust-accept-btn-handler'
    __dev_mode = True
   
    def __init__(self, hyperlink = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_update = True
        self.page_load_treshold = global_settings['webpage_load_treshold']
        self.max_attempts_treshold = global_settings['max_attempts_treshold']
        self.chrome_options = webdriver.ChromeOptions()
        self.__set_chrome_options()
        self.hyperlink = hyperlink

    @property
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, new_value):
        if new_value:
            self._hyperlink = new_value
            self.hyperlink_update()

    def hyperlink_update(self):
        self.time_out_counter = 0
        self.__get_page()
    
    def __set_chrome_options(self):
        self.chrome_options.add_argument('keep_alive')
        if not PreparePageSource.__dev_mode:
            self.chrome_options.add_argument('headless')

    def __get_page(self):
        if self.first_update:
            self.first_update = False
            self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                            options = self.chrome_options)
            logger_object.log('Driver initialization complete', 'DEBUG')
        try:
            self.driver.get(self.hyperlink)
            logger_object.log(f'Page {self.hyperlink} loaded', 'INFO')
        except Exception as e:
            logger_object.log(f'Page {self.hyperlink} unable to load, exception {e} occure', 'ERROR')
        self.wait_for_page_to_load()
        self.__click_cookie_button()


    def page_content(self):
        self.wait_for_page_to_load()
        return BeautifulSoup(self.driver.page_source, 'lxml')

    def __click_cookie_button(self):
        self.driver.implicitly_wait(self.page_load_treshold)
        try:
            (self.driver.find_element_by_id(PreparePageSource.__cookie_button_name)).click()
            logger_object.log(f'Cookie button clicked', 'DEBUG')
        except Exception as e:
            logger_object.log(f'Cookie button unable to find on page {self.hyperlink}, exception {e} occure', 'WARNING')

    def wait_for_page_to_load(self):
        self.time_out_counter = 0
        while not self.driver.execute_script("return document.readyState") == 'complete':
            time.sleep(0.2)
            self.time_out_counter+=1

            if self.time_out_counter > self.max_attempts_treshold:
                raise PageTimedOut('Unable to fully load page.')
        logger_object.log(f'Page ready', 'DEBUG')

    def __str__(self):
        return f'Prepared page source from hyperlink: {self.hyperlink}'

    def __repr__(self):
        return f'PreparePageSource({self.hyperlink})'
