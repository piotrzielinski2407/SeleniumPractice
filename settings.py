from files_handling import load_JSON

def load_settings():
    """
    function that will load settings file and return dict with settings
    """
    return load_JSON('global_settings.json')

def load_DB_config():
    """
    Funtion that will load configuration to database connections
    """
    return load_JSON('db_settings.json')
   
