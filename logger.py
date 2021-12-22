from singleton import Singleton
from threading_lock import data_lock
import logging
from aditional_functions import set_directory

class Logger(metaclass = Singleton):
    '''
    Class for logging events, only one for whole software (Singleton)
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(filename='summary.log', filemode='w', 
                            format='%(asctime)s %(message)s', level = logging.INFO
                            )
    def log(self, message, event):
        data_lock.acquire()
        logging.info(event.upper() + ' : ' + message)
        data_lock.release()
        
set_directory()
logger_object = Logger()

if __name__ == '__main__':
    #some testing here
    x = Logger()
    y = Logger()

    x.log('test1', 'INFO')
    y.log('test2', 'DEBUG')
    