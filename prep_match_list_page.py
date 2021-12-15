from webpageprep import PreparePageSource

class PrepareMatchListPage(PreparePageSource):
    __show_more_tracker = 'Show more matches'
    
    def __init__(self, hyperlink):
        super().__init__(hyperlink)

    def __load_all_matches(self):
        