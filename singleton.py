class Singleton(type):
    _instance = None
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance

def singleton_wrapper(cls):    
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper
