import psycopg2
from settings import load_DB_config
from logger import logger_object
#from aditional_functions import set_directory
#set_directory()
config = load_DB_config()

class DB():
    """
    Class that will provide nescesary methods to provide communication with DB - adapter design pattern
    This class is designed as multipurpouse and universal to all future usage of postgressSQL.
    Many operation will double check if table exist to avoid situation that someone else or other part 
    of software change something in DB
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.conn = psycopg2.connect(database=config["db_name"], user=config["user"], password=config["password"], host=config["host"], port=config["port"])
            self.cur = self.conn.cursor()
            logger_object.log('Connection with DB sucesfull', 'INFO')
        except Exception as e:
            logger_object.log(f'Exception occure during estabilishing connection with DB: {e}', 'ERROR')
        self.active_table = None

    def create_table(self, table_name, column_parameters = None, table_constraints = None):
        '''
        Method that will create table with columns in it only if column_parameters is provided, otherwise only empty table is created.
        Make that table active one.
        For columns creation data see method define_columns
        '''
        if not self.is_table_exist(table_name):
            sql = f"CREATE TABLE {table_name} ();"
            self.cur.execute(sql)
            self.active_table = table_name
            logger_object.log(f'Table "{table_name}" created', 'DEBUG')
            return True
        logger_object.log(f'Table with that name:"{table_name}" already exist or no table name provided', 'WARNING')
        return False

    def rename_table(self, new_table_name, table_name = None):
        '''
        Method that will change table name for other, if no table_name provided, active on will be taken into consideration
        Table with new name become active one
        Return True if everything passed withoud errors
        '''
        result = self.__table_name_set(table_name)#checking if active or provided table exist
        if result is not False:
            table_name = result
        else:
            return False
            
        if not self.is_table_exist(new_table_name):#chec if new table name is availible
            sql = f"ALTER TABLE {table_name} RENAME TO {new_table_name};"
            self.cur.execute(sql)
            logger_object.log(f'Sucess {table_name} changed name to {new_table_name} and become active', 'INFO')
            self.active_table = new_table_name
            return True
        logger_object.log(f'Unable to changed name of {table_name} to {new_table_name}, {new_table_name} is already used ', 'ERROR')
        return False 

    def add_columns(self, columns_parameters, table_name = None):
        '''
        Method that will add columns to table, if no table_name is provided current table is taken into consideration.
        columns variable should be list of 3 elements lists: 1el-column name,   2el-datatype, 3el-column constraint.
        '''
        result = self.__table_name_set(table_name)#checking if active or provided table exist
        logger_object.log(f'TEST {result}', 'DEBUG')
        if result is not False:
            table_name = result
        else:
            logger_object.log(f'Table {table_name} not found in DB', 'DEBUG')
            return False
        
        if isinstance(columns_parameters, list) and isinstance(columns_parameters[0], list):
            sql_command = self.__sql_command_add_column(columns_parameters, table_name)
            if sql_command is not False:
                sql = sql_command
            else:
                return False#exception already raised in __sql_command_add_column
            try:
                self.cur.execute(sql)
            except Exception as e:
                logger_object.log(f'Exception: {e} occure durign adding columns', 'ERROR')
                return False
            logger_object.log('Columns added', 'DEBUG')
            return True
        logger_object.log('Column parametrs should be type of list', 'ERROR')
        return False        
                

    def __sql_command_add_column(self, columns_parameters, table_name):
        sql = f'ALTER TABLE {table_name}'
        try:
            for column_param in columns_parameters:
                sql = sql + \
                f' ADD COLUMN {column_param[0]} {column_param[1]} {column_param[2]},'
            return sql[:len(sql) - 1] + ';'
        except Exception as e:
            logger_object.log(f'Exception: {e} occured during creating sql command ', 'ERROR')
            return False


    def __table_name_set(self, table_name):
        '''
        Inside method only to check if provided table name exist in db, if not active table is checked
        Return correct table name if it is true, return false and log error if not.
        '''
        if table_name is None:
            if self.is_table_exist() is not False: 
                return self.active_table
            return False

        if self.is_table_exist(table_name) is not False:
            return table_name
        return False

    def activate_table(self, table_name):
        pass


    def is_table_exist(self, table_name=None):
        '''
        Method that will check if table exist in DB, if no table_name provided active table will be checked
        If error occured None will be returned
        '''
        if table_name is None:
            if self.active_table is not None:
                table_name = self.active_table
            else:
                logger_object.log(f'Active table is not set, no table to check if exist' 'ERROR')
                return False
        self.cur.execute(f"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = '{table_name}');")
        result = self.cur.fetchone()[0]
        logger_object.log(f'Execute test if {table_name} in DB with result {result}', 'DEBUG')
        return result

    def __exit__(self):

        try:
            self.cur.close()
            logger_object.log('DB cursor closed sucesfull', 'INFO')
        except Exception as e:
            logger_object.log(f'Exception occure during closing DB cursor: {e}', 'ERROR')

        try:
            self.conn.close()
            logger_object.log('DB connection closed sucesfull', 'INFO')
        except Exception as e:
            logger_object.log(f'Exception occure during closing DB connection: {e}', 'ERROR')
        
    def __str__(self):
        return 'Connection with DB provider'

    def __repr__(self):
        return 'DB()'

    def __exit__(self):
        try:
            self.conn.commit()
        except:
            pass
        try:
            self.conn.close()
        except:
            pass


if __name__ == '__main__':
    #some testing here  
    table_name = 'test3'
    db = DB()

    column_parameters = [
                        ['id', 'SERIAL', 'PRIMARY KEY'],
                        ['column_2', 'varchar(10)', 'NOT NULL'],
                        ['column_3', 'varchar(10)', 'NOT NULL']
                        ]

    db.rename_table('test5','test3')



