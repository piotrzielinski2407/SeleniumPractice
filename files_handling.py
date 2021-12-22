from logger import logger_object
import json

def load_JSON(file_to_load):
    """
    findtion that will load JSON file and return dict
    """
    try:
        with open(file_to_load,'r') as settings:
           settings_dict = json.load(settings)
        settings.close()
        logger_object.log(f'File {file_to_load} loaded corectly', 'INFO')
        return settings_dict
    except Exception as e:
        logger_object.log(f'Exception occured: {e} during loading file {file_to_load}', 'ERROR')