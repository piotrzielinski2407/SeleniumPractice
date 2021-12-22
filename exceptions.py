class PageTimedOut(Exception):
    '''Raise when driver was unable to fully load a page.'''
    pass

class WrongDateException(Exception):
    '''Exception raised when wrong date was provided by user'''
    pass