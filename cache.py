from singleton import Singleton
from threading_lock import data_lock

class CacheHistory(metaclass = Singleton):
    history = {}
    def __init__(self):
        pass

    def team_ticker_update(self, league):
        pass#here should be method to download all known tickers for team in league

cache_history = CacheHistory()

def cache(method):
    def wrapper(self, x):
        data_lock.acquire()
        if x not in cache_history.history:
            cache_history.history[x] = method(self, x)
            print('saved in cache')
        print('return from cache')
        data_lock.release()
        return cache_history.history[x] 
    return wrapper


if __name__ == '__main__':
    #some testing here  

    class test():
        def __init__(self):
            pass
        
        @cache
        def some_method(self, x):
            return 2*x

 
    x = test()

    print(x.some_method(2))

    print(x.some_method(2))