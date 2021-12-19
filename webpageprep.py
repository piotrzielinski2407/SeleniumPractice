from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from exceptions import *
from logger import Logger


class PreparePageSource(Logger):
    '''
    Base class to preapre page before scrapping, might be parent to other more complex clases
    '''
    __cookie_button_name = 'onetrust-accept-btn-handler'
    __dev_mode = True
    __time_out_treshold = 500 #maximum attempts to fully load page

    def __init__(self, hyperlink, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_update = True
        self.chrome_options = webdriver.ChromeOptions()
        self.__set_chrome_options()
        self.hyperlink = hyperlink

    @property
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, new_value):
        self._hyperlink = new_value
        self.hyperlink_update()

    def hyperlink_update(self):
        if not self.first_update:
            try:#if no window is present, error occur and should be passed
                self.driver.close()
                self.log('Driver closed properly', 'INFO')
            except Exception as e:
                self.log(f'Exception occure: {e}', 'WARNING')
                pass
        self.first_update = False
        self.driver = None
        self.time_out_counter = 0
        self.__get_page()
    
    def __set_chrome_options(self):
        self.chrome_options.add_argument('keep_alive')
        if not PreparePageSource.__dev_mode:
            self.chrome_options.add_argument('headless')

    def __get_page(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                        options = self.chrome_options)
        self.log('Driver initialization complete', 'DEBUG')
        self.driver.get(self.hyperlink)
        self.log(f'Page {self.hyperlink} loaded', 'INFO')
        self.wait_for_page_to_load()
        self.__click_cookie_button()


    def page_content(self):
        self.wait_for_page_to_load()
        return BeautifulSoup(self.driver.page_source, 'lxml')

    def __click_cookie_button(self):
        self.driver.implicitly_wait(10)
        (self.driver.find_element_by_id(PreparePageSource.__cookie_button_name)).click()
        self.log(f'Cookie button clicked', 'DEBUG')

    def wait_for_page_to_load(self):
        self.time_out_counter = 0
        while not self.driver.execute_script("return document.readyState") == 'complete':
            time.sleep(0.2)
            self.time_out_counter+=1

            if self.time_out_counter > PreparePageSource.__time_out_treshold:
                raise PageTimedOut('Unable to fully load page.')
        self.log(f'Page ready', 'DEBUG')

    def __str__(self):
        return f'Prepared page source from hyperlink: {self.hyperlink}'

    def __repr__(self):
        return f'PreparePageSource({self.hyperlink})'
