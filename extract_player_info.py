from webpageprep import PreparePageSource
from aditional_functions import DateHandler
from logger import logger_object

class ScrapPlayerInfo(PreparePageSource):

    player_name_div_name = 'heading__name'
    player_current_position_div_name = 'heading__info--type-name'
    player_age_div_name = 'heading__info--birthdate'
    player_height_div_name = 'heading__info--height'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hyperlink = None
        self.return_list = []

    def scrap_it(self):
        self.return_list = []
        if self.hyperlink is not None:
            self.page = self.page_content()
            self.__player_id_extraction()
            self.__scrap_name()
            self.__scrap_position()
            self.__scrap_age()
            self.__scrap_height()
            self.return_list.append(self.hyperlink)

    def __exception_cacher(method):
        def wrapper(self):
            try:
                method(self)
            except Exception as e:
                self.return_list.append('N/A')
                logger_object.log(f'Exception occured: {e}', 'ERROR')
           
        return wrapper

    @__exception_cacher
    def __player_id_extraction(self):
        href = self.hyperlink
        player_id  = href[href[:-1].rfind('/')+1:-1]
        self.return_list.append(player_id)

    @__exception_cacher
    def __scrap_name(self):
        name = self.page.find('div', class_ = ScrapPlayerInfo.player_name_div_name).get_text().strip()
        self.return_list.append(name)

    @__exception_cacher
    def __scrap_position(self):
        position_raw = self.page.find('div', class_ = ScrapPlayerInfo.player_current_position_div_name).get_text().strip()
        hidden_char_position = position_raw.find('\xa0')
        
        if hidden_char_position != -1:
            position = position_raw[:hidden_char_position]
        else:
            position = position_raw
        self.return_list.append(position)
            
    @__exception_cacher
    def __scrap_age(self):
        age_raw = self.page.find('div', class_ = ScrapPlayerInfo.player_age_div_name).get_text().strip()
        date_procesor = DateHandler(date = age_raw[9:len(age_raw)-1], date_format="%d.%m.%Y")
        birth_date = date_procesor.return_date()
        self.return_list.append(birth_date)

    @__exception_cacher
    def __scrap_height(self):
        height_raw = self.page.find('div', class_ = ScrapPlayerInfo.player_height_div_name).get_text().strip()
        height = height_raw[8:len(height_raw)-3]
        self.return_list.append(height)


if __name__ == '__main__':
    #some testing here
    test_list = ['https://www.flashscore.com/player/randolph-anthony/K65yzyGs/', 'https://www.flashscore.com/player/sakho-jordan/MobAQKET/',
    'https://www.flashscore.com/player/koumadje-christ/tIqF5GLI/', 'https://www.flashscore.com/player/dominiguez-ruben/MFddmK0J/']
    
    
    playerinfo = ScrapPlayerInfo()
    data1= []
    for link in test_list:
        playerinfo.hyperlink = link
        playerinfo.scrap_it()
        data1.append(playerinfo.return_list)
    
    playerinfo.driver.close()
    from pandas_columns_name import pandas_players_info_columns_names
    import pandas as pd

    df= pd.DataFrame(data = data1)
    df.columns = pandas_players_info_columns_names
    print(df)
 
    


