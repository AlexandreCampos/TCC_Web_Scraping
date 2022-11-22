import mysql.connector


DATABASE_NAME = "projeto_scrapper"
HOST="localhost"
USER="root"
PASSWORD="root"

def connect():
    '''
    Database connection.

    Returns:
        con (CMySQLConnection): Object MySQL Connection
        cursor (CMySQLCursor): Object MySQL Cursor
    '''

    con = mysql.connector.connect(
      host=HOST,
      user=USER,
      password=PASSWORD,
      database=DATABASE_NAME
    )
    cursor = con.cursor()
    
    return con, cursor


class SimpleQuery(object):
    ''' Class for queries.'''

    def create_database(self, name, verify=True):
        '''
        Query to create database.

        Args:
            name (str): Database name
            verify (boolean): Verify if database exists

        Returns:
            created (boolean): The result of query
        '''

        if verify:
            query = "CREATE DATABASE IF NOT EXISTS {}".format(name)
        else:
            query = "CREATE DATABASE {}".format(name)
        try:
            mydb = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWORD
            )
            cursor = mydb.cursor()
            cursor.execute(query)
            return True
        except mysql.connector.Error as e:
            print(f"Falha ao criar database: {e}")
            return False
        finally:
            cursor.close()

    def table_exists(self, name):
        '''
        Validate if table exists.

        Args:
            name (str): Database name

        Returns:
            exists (int): Code with result
        '''
        
        try:
            result = self.select(
                """
                    SELECT * 
                    FROM information_schema.tables
                    WHERE table_schema = '{database}' 
                        AND table_name = '{name}'
                    LIMIT 1;
                """.format(
                        name=name,
                        database=DATABASE_NAME
                    )
            )
            if result:
                return 1
            else:
                return 0
        except Exception as e:
            print(f"Falha ao verificar se tabela existe: {e}")
            return -1        

    def create_table(self, query):
        '''
        Query to create table.

        Args:
            query (str): Create table query

        Returns:
            created (boolean): The result of query
        '''
        
        try:
            con, cursor = connect()
            cursor.execute(query)    
            return True
        except mysql.connector.Error as e:
            print(f"Falha ao criar tabela: {e}")
            return False
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def alter_table(self, query):
        '''
        Query to alter table.

        Args:
            query (str): Alter table query

        Returns:
            created (boolean): The result of query
        '''
        
        try:
            con, cursor = connect()
            cursor.execute(query)    
            return True
        except mysql.connector.Error as e:
            print(f"Falha ao alterar tabela: {e}")
            return False
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def insert(self, query, values):
        '''
        Query to insert.

        Args:
            query (str): Insert query
            values (tuple): Tuple with values

        Returns:
            inserted (boolean): The result of query
        '''
        
        try:
            con, cursor = connect()
            cursor.executemany(query, values)
            con.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Falha ao inserir dados: {e}")
            return False
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def update(self, query, values=None):
        '''
        Query to update.

        Args:
            query (str): Update query
            values (tuple): Tuple with values

        Returns:
            updated (boolean): The result of query
        '''
        
        try:
            con, cursor = connect()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            con.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Falha ao atualizar dados: {e}")
            return False
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def delete(self, query):
        '''
        Query to delete.

        Args:
            query (str): Delete query
        
        Returns:
            deleted (boolean): The result of query
        '''
        
        try:
            con, cursor = connect()
            cursor.execute(query)
            con.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Falha ao deletar dados: {e}")
            return False
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def select(self, query, values=None):
        '''
        Query to select.

        Args:
            query (str): Select query
            values (tuple): Tuple with values

        Returns:
            result (list): The result of query
        '''
        
        try:
            con, cursor = connect()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            columns = cursor.description 
            result = [
                {
                    columns[index][0]:column
                    for index, column in enumerate(value)
                }
                for value in cursor.fetchall()
            ]
            return result        
        except mysql.connector.Error as e:
            print(f"Falha ao selecionar dados: {e}")
            return []
        finally:
            if con.is_connected():
                cursor.close()
                con.close()


class TransactionQuery(object):
    ''' Class for queries with transaction.'''

    def select(self, cursor):
        '''
        Get data from result of select query.

        Args:
            cursor (CMySQLCursor): Object MySQL Cursor

        Returns:
            result (list): The result of query
        '''
        
        columns = cursor.description 
        result = [
            {
                columns[index][0]:column
                for index, column in enumerate(value)
            }
            for value in cursor.fetchall()
        ]
        return result

    def execute_transaction(self):
        '''
        Run multiple queries with transaction, using functions of
        mysql.connector library. 
        If all queries are executed correctly, then commit, if not, rollback.
        '''
        
        try:
            con, cursor = connect()
            con.autocommit = False
            self.execute_queries(cursor)
            con.commit()
            return True
        except mysql.connector.Error as e:
            con.rollback()
            print(f"Falha ao executar a operação. Realizado o rollback. Erro: {e}")
            return False
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def execute_queries(self):
        raise NotImplementedError

