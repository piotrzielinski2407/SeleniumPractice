import os
import datetime

def set_directory():
    scriptDir = os.path.dirname(__file__)
    os.chdir(scriptDir)

class DateHandler():
    def __init__(self, date = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if date:
            self.set_date(date)
        else:
            self.date = None
            self.year = None
            self.month = None
            self.day = None

    def set_date(self, new_value):
        self.date = datetime.datetime.strptime(new_value, "%Y.%m.%d")
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day



if __name__ == '__main__':
    #some testing here  

    test = DateHandler(date = "2018.10.11")
    #test.set_date("2018.10.11")
    print(test.year)