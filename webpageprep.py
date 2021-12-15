from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from exceptions import *


class PreparePageSource():
    '''
    Base class to preapre page before scrapping, might be parent to other more complex clases
    '''
    __cookie_button_name = 'onetrust-accept-btn-handler'
    __dev_mode = True
    __time_out_treshold = 500 #maximum attempts to fully load page

    def __init__(self, hyperlink, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hyperlink = hyperlink
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = None
        self.time_out_counter = 0
        self.__get_page()
    
    def __set_chrome_options(self):
        self.chrome_options.add_argument('keep_alive')
        if not PreparePageSource.__dev_mode:
            self.chrome_options.add_argument('headless')

    def __get_page(self):
        self.__set_chrome_options()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                        options = self.chrome_options)
        self.driver.get(self.hyperlink)
        self.wait_for_page_to_load()
        self.__click_cookie_button()

    def page_content(self):
        self.wait_for_page_to_load()
        return BeautifulSoup(self.driver.page_source, 'lxml')

    def __click_cookie_button(self):
        (self.driver.find_element_by_id(PreparePageSource.__cookie_button_name)).click()

    def wait_for_page_to_load(self):
        self.time_out_counter = 0
        while not self.driver.execute_script("return document.readyState") == 'complete':
            time.sleep(0.2)
            self.time_out_counter+=1

            if self.time_out_counter > PreparePageSource.__time_out_treshold:
                raise PageTimedOut('Unable to fully load page.')

    def __str__(self):
        return f'Prepared page source from hyperlink: {self.hyperlink}'

    def __repr__(self):
        return f'PreparePageSource({self.hyperlink})'
