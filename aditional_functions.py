import os
import datetime

def set_directory():
    scriptDir = os.path.dirname(__file__)
    os.chdir(scriptDir)

class DateHandler():
    '''
    Class that will provide separate day, month, year based on provided argument
    '''
    def __init__(self, date = None, date_format = "%Y.%m.%d", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_format = date_format
        self.date_default_format = "%Y.%m.%d"
        if date:
            self.set_date(date)
        else:
            self.date = None
            self.year = None
            self.month = None
            self.day = None

    def set_date(self, new_value):
        self.date = datetime.datetime.strptime(new_value, self.date_format)
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day

    def return_date(self):
        '''
        Function that will return date in default date format 
        '''
        return self.date.strftime(format = self.date_default_format)


def substract_list_content(origin_list, check_list):
    origin_set = set(origin_list)
    temp_set = origin_set.difference(check_list)
    return list(temp_set)

if __name__ == '__main__':
    #some testing here  
    lista1 = ['A', 'B', 'C', 'D']

    lista2 = ['C', 'D']

    print(substract_list_content(lista1, lista2))