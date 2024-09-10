import mysql.connector
from src.main.model.dao.dao.i_dao import IDAO
from src.main.model.connection.mysql_connection import MySQLConnection

class DAOImpl(IDAO):
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        
    def execute_select(self, select_query, attributes=()):
        try:
            results_set = None
            if attributes == ():
                self.cursor.execute(select_query)
            else:
                self.cursor.execute(select_query, attributes)
            results_set = self.cursor.fetchall()
            if results_set is None:
                return []
            return results_set
        except mysql.connector.Error as e:
            error = f"errore. {e}"
            raise Exception(error)
        
    def execute_action(self, query, attributes=(), num_tuples_consider=0):
        try:
            if attributes == ():
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, attributes)
            if num_tuples_consider != self.cursor.rowcount:
                raise mysql.connector.Error()
            return True
        except mysql.connector.Error as e:
            error = f"errore. {e}"
            raise Exception(error)









