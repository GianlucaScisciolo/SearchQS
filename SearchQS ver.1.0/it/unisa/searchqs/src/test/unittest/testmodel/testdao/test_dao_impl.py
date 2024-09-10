import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.dao.dao_impl import DAOImpl
import mysql

class TestDAOImpl(unittest.TestCase):    
    """ Test init """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)

    """ Test execute_select """

    def test_2_execute_select_with_attributes_results_success(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_select_query = "SELECT name, surname, year_birth FROM user WHERE year_birth >= %s;"
        test_attributes = (40,)
        oracle = [("Mario", "Rossi", 1980), ("Laura", "Verdi", 1960), ("Gianni", "Bianchi", 1960)]
        dao.cursor.fetchall.return_value = [("Mario", "Rossi", 1980), ("Laura", "Verdi", 1960), 
                                                 ("Gianni", "Bianchi", 1960)]
        result = dao.execute_select(test_select_query, test_attributes)
        self.assertEqual(result, oracle)

    def test_3_execute_select_without_attributes_results_success(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_select_query = "SELECT name, surname, year_birth FROM user WHERE year_birth >= 40;"
        test_attributes = ()
        oracle = [("Mario", "Rossi", 1980), ("Laura", "Verdi", 1960), ("Gianni", "Bianchi", 1960)]
        dao.cursor.fetchall.return_value = [("Mario", "Rossi", 1980), ("Laura", "Verdi", 1960), 
                                                 ("Gianni", "Bianchi", 1960)]
        result = dao.execute_select(test_select_query, test_attributes)
        self.assertEqual(result, oracle)

    def test_4_execute_select_with_attributes_not_result_success(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_select_query = "SELECT name, surname, year_birth FROM user WHERE year_birth >= %s;"
        test_attributes = (40,)
        oracle = []
        dao.cursor.fetchall.return_value = None
        result = dao.execute_select(test_select_query, test_attributes)
        self.assertEqual(result, oracle)

    def test_5_execute_select_without_attributes_not_result_success(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_select_query = "SELECT name, surname, year_birth FROM user WHERE year_birth >= 40;"
        test_attributes = ()
        oracle = []
        dao.cursor.fetchall.return_value = None
        result = dao.execute_select(test_select_query, test_attributes)
        self.assertEqual(result, oracle)

    def test_6_execute_select_with_attributes_exception(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_select_query = "SELECT name, surname, year_birth FROM user WHERE year_birth >= %s;"
        test_attributes = (40,)
        dao.cursor.execute.side_effect = mysql.connector.Error("errore durante l\'esecuzione della select.")
        with self.assertRaises(Exception) as context:
            dao.execute_select(test_select_query, test_attributes)
        self.assertTrue("errore durante l\'esecuzione della select." in str(context.exception))

    def test_7_execute_select_without_attributes_exception(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_select_query = "SELECT name, surname, year_birth FROM user WHERE year_birth >= 40;"
        test_attributes = ()
        dao.cursor.execute.side_effect = mysql.connector.Error("errore durante l\'esecuzione della select.")
        with self.assertRaises(Exception) as context:
            dao.execute_select(test_select_query, test_attributes)
        self.assertTrue("errore durante l\'esecuzione della select." in str(context.exception))

    """ Test execute_action """

    def test_8_execute_action_with_attributes_success(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_query = "DELETE FROM registered_user WHERE year_birth > %s;"
        test_attributes = (101,)
        test_num_tuples_consider = 1
        dao.cursor.rowcount = 1
        result = dao.execute_action(test_query, test_attributes, test_num_tuples_consider)
        self.assertTrue(result)

    def test_9_execute_action_without_attributes_success(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_query = "DELETE FROM registered_user WHERE year_birth > 101;"
        test_attributes = ()
        test_num_tuples_consider = 1
        dao.cursor.rowcount = 1
        result = dao.execute_action(test_query, test_attributes, test_num_tuples_consider)
        self.assertTrue(result)

    def test_10_execute_action_with_attributes_exception(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_query = "DELETE FROM registered_user WHERE year_birth > %s;"
        test_attributes = (101,)
        test_num_tuples_consider = 1
        dao.cursor.rowcount = 0
        with self.assertRaises(Exception) as context:
            dao.execute_action(test_query, test_attributes, test_num_tuples_consider)
        self.assertTrue("errore" in str(context.exception))

    def test_11_execute_action_without_attributes_exception(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = DAOImpl(connection.connection, connection.cursor)
        test_query = "DELETE FROM registered_user WHERE year_birth > 101;"
        test_attributes = ()
        test_num_tuples_consider = 1
        dao.cursor.rowcount = 0
        with self.assertRaises(Exception) as context:
            dao.execute_action(test_query, test_attributes, test_num_tuples_consider)
        self.assertTrue("errore" in str(context.exception))










