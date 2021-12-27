import psycopg2
from settings import load_DB_config
from logger import logger_object
config = load_DB_config()

class DB():
    """
    Class that will provide nescesary methods to provide communication with DB - adapter design pattern
    This class is designed as multipurpouse and universal to all future usage of postgressSQL.
    Many operation will double check if table exist to avoid situation that someone else or other part 
    of software change something in DB
    Any operation on slected table make it active one
    Any intance fo this should be used with "with" statement to allow safe connecion close, otherwise, 
    methods close_cur and close_conn should be called manually
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.__conn = psycopg2.connect(database=config["db_name"], user=config["user"], password=config["password"], host=config["host"], port=config["port"])
            self.__cur = self.__conn.cursor()
            logger_object.log('Connection with DB sucesfull', 'INFO')
        except Exception as e:
            logger_object.log(f'Exception occure during estabilishing connection with DB: {e}', 'ERROR')
        self.active_table = None
    
    def __commit_after(method):
        def wrapper(self, *args, **kwargs):
            method(self, *args, **kwargs)
            self.commit()
        return wrapper

    def __execute_with_log(method):
        def wrapper(self, *args, **kwargs):
            try:
                result = method(self, *args, **kwargs)
                logger_object.log(f'Method "{method.__name__}" executed corectly', 'INFO')
                return result
            except Exception as e:
                logger_object.log(f'Exception {e} occured during executing "{method.__name__}"', 'ERROR')
                return False
        return wrapper
    
    def __table_set(method):
        def wrapper(self, *args, table_name = None, **kwargs):
            if table_name is None:
                if self.is_table_exist() is not False: 
                    return method(self, *args, **kwargs)
                return False

            if self.is_table_exist(table_name) is not False:
                self.active_table = table_name
                return method(self, *args, **kwargs)
            return False
        return wrapper

    @__execute_with_log
    def execute(self, sql):
        return self.__cur.execute(sql)   
    
    @__execute_with_log
    def fetchone(self):
        return self.__cur.fetchone()

    @__execute_with_log
    def fetchmany(self, rows):
        return self.__cur.fetchmany(rows)

    @__execute_with_log
    def fetchall(self):
        return self.__cur.fetchall()

    @__execute_with_log
    def close_conn(self):
        self.__conn.close()

    @__execute_with_log
    def commit(self):
        self.__conn.commit()
        
    @__execute_with_log
    def close_cur(self):
        self.__cur.close()

    @__commit_after
    def create_table(self, table_name, column_parameters = None):
        '''
        Method that will create table with columns in it only if column_parameters is provided, otherwise only empty table is created.
        Make that table active one.
        For columns creation data see method define_columns
        '''
        if not self.is_table_exist(table_name):
            sql = f"CREATE TABLE {table_name} ();"
            self.execute(sql)
            self.active_table = table_name
            logger_object.log(f'Table "{table_name}" created', 'DEBUG')
            if column_parameters is not None:
                return self.add_columns(column_parameters, table_name = self.active_table)
            return True
        logger_object.log(f'Table with that name:"{table_name}" already exist or no table name provided', 'WARNING')
        return False

    @__commit_after
    @__table_set
    def rename_table(self, new_table_name, table_name = None):
        '''
        Method that will change table name for other, if no table_name provided, active on will be taken into consideration
        Table with new name become active one
        Return True if everything passed withoud errors
        '''
        if not self.is_table_exist(new_table_name):#check if new table name is availible
            sql = f"ALTER TABLE {self.active_table} RENAME TO {new_table_name};"
            self.execute(sql)
            logger_object.log(f'Sucess {self.active_table} changed name to {new_table_name} and become active', 'DEBUG')
            self.active_table = new_table_name
            return True
        logger_object.log(f'Unable to changed name of {self.active_table} to {new_table_name}, {new_table_name} is already used ', 'ERROR')
        return False 

    @__commit_after
    @__table_set     
    def drop_table(self, table_name = None):
        '''
        Method that will drop table table_name if no table_name is provided, active table is taken into consideration
        '''
        sql = f'DROP TABLE {self.active_table}'
        self.execute(sql)
        return True

    @__table_set
    def add_columns(self, columns_parameters, table_name = None):
        '''
        Method that will add columns to table, if no table_name is provided current table is taken into consideration.
        columns variable should be list of 3 elements lists: 1el-column name,   2el-datatype, 3el-column constraint.
        '''
        return self.__column_operation('ADD', columns_parameters)
    
    @__table_set
    def remove_columns(self, columns_names, table_name = None):
        '''
        Method that will remove column/s from table 
        Column names should be list of lists to proper functioning
        '''
        return self.__column_operation('DROP', columns_names)
    
    @__commit_after
    def __column_operation(self, opearation, columns_parameters):
        '''
        Universal method to operate on columns
        '''
        if isinstance(columns_parameters, list) and isinstance(columns_parameters[0], list):
            sql_command = self.__sql__column_operation(opearation, columns_parameters, self.active_table)
            if sql_command is not False:
                sql = sql_command
            else:
                return False#exception already raised in __sql_command_add_column
            
            if self.execute(sql) is not False:
                logger_object.log('Columns added', 'DEBUG')
                return True
            return False
        logger_object.log('Column parametrs should be type of list', 'ERROR')
        return False   

    @__execute_with_log
    def __sql__column_operation(self, opearation, columns_parameters, table_name):
        '''
        Column operation like: ADD, DROP, ALTER
        '''
        sql = f'ALTER TABLE {table_name}'
        for column_param in columns_parameters:
            sql = sql + f' {opearation} COLUMN'
            for param in column_param:
                sql = sql + f' {param}'
            sql = sql + ','
        return sql[:len(sql) - 1] + ';'

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
        self.execute(f"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = '{table_name}');")
        result = self.fetchone()[0]
        logger_object.log(f'Execute test if {table_name} in DB with result {result}', 'DEBUG')
        return result
    
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close_cur()
        self.close_conn()
        logger_object.log(f'Connection with DB ended', 'INFO')
        
    def __str__(self):
        return 'Connection with DB provider'

    def __repr__(self):
        return 'DB()'

if __name__ == '__main__':
    #some testing here  
    table_name2 = 'test48'
    

    column_parameters = [
                        ['id', 'SERIAL', 'PRIMARY KEY'],
                        ['column_2', 'varchar(10)', 'NOT NULL'],
                        ['column_3', 'varchar(10)', 'NOT NULL']
                        ]

    with DB() as db:
        db.active_table = table_name2
        db.create_table('test50',column_parameters)



