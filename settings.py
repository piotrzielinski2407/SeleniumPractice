from files_handling import load_JSON

def load_settings():
    """
    function that will load settings file and return dict with settings
    """
    return load_JSON('global_settings.json')

def load_hyperlink_settings():
    '''
    Function that will load data nescessary for hyperlinks to season summary creation and return dict
    '''
    return load_JSON('hyperlink_settings.json')

def load_DB_config():
    """
    Funtion that will load configuration to database connections
    """
    return load_JSON('db_settings.json')
   
