import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import patch, Mock, MagicMock
from src.main.model.connection.mysql_connection import MySQLConnection
import mysql.connector

class TestMySQLConnection(unittest.TestCase):
    def test_1_init(self):
        connection = MySQLConnection()
        self.assertIsNone(connection.connection)
        self.assertIsNone(connection.cursor)

    def test_2_open_success(self):
        with patch('mysql.connector.connect') as mock_connect:
            connection = MySQLConnection()
            
            mock_connect.return_value.cursor.return_value = MagicMock()

            result = connection.open()
            
            self.assertTrue(result)
            mock_connect.assert_called_once_with(
                host="localhost",
                user="da_inserire",
                password="da_inserire",
                database="testsearchqs" # oppure searchqs se non testiamo
            )
            is_closed = connection.close()
            self.assertTrue(is_closed)

    def test_3_open_failure(self):
        with patch('mysql.connector.connect') as mock_connection:
            mock_connection.side_effect = mysql.connector.Error("Si è verificato un errore durante la connessione al database.")
            connection = MySQLConnection()
            result = connection.open()

            self.assertFalse(result)
            self.assertEqual(mock_connection.call_count, 1)

    def test_4_close_success(self):
        with patch('mysql.connector.connect') as mock_connect:
            connection = MySQLConnection()
            mock_connect.return_value.cursor.return_value = MagicMock()
            result = connection.open()
            self.assertTrue(result)
            result = connection.close()
            self.assertTrue(result)

    def test_5_close_failure(self):
        with patch('mysql.connector.connect') as mock_connection:
            connection = MySQLConnection()
            result = connection.open()
            self.assertTrue(result)
            mock_connection.return_value.close.side_effect = mysql.connector.Error("Si è verificato un errore durante la chiusura della connessione al database.")
            result = connection.close()
            self.assertFalse(result)

    def test_6_fetchall(self):
        with patch('mysql.connector.connect') as mock_connection:
            connection = MySQLConnection()
            mock_connection.return_value.cursor.return_value.fetchall.return_value = ['risultato 1', 'risultato 2']
            connection.open()
            result = connection.fetchall()
            connection.close()
            oracle = ['risultato 1', 'risultato 2']

            self.assertEqual(result, oracle)
            self.assertEqual(mock_connection.call_count, 1)

    def test_7_commit(self):
        with patch('mysql.connector.connect') as mock_connection:
            connection = MySQLConnection()
            mock_connection.return_value.cursor.return_value.commit.return_value = True
            connection.open()
            result = connection.commit()
            connection.close()
            
            self.assertTrue(result)
            self.assertEqual(mock_connection.call_count, 1)

    def test_8_rollback(self):
        with patch('mysql.connector.connect') as mock_connection:
            connection = MySQLConnection()
            mock_connection.return_value.rollback.return_value = True
            connection.open()
            result = connection.rollback()
            connection.close()
            oracle = ['risultato 1', 'risultato 2']
            
            self.assertTrue(result)
            self.assertEqual(mock_connection.call_count, 1)

    def test_9_start_transaction(self):
        with patch('mysql.connector.connect') as mock_connection:
            connection = MySQLConnection()
            mock_connection.return_value.start_transaction.return_value = True
            connection.open()
            result = connection.start_transaction()
            connection.close()

            self.assertTrue(result)
            self.assertEqual(mock_connection.call_count, 1)

    def test_10_rowcount(self):
        with patch('mysql.connector.connect') as mock_connection:
            connection = MySQLConnection()
            mock_connection.return_value.cursor.return_value.rowcount = 5
            connection.open()
            result = connection.rowcount()
            connection.close()
            oracle = 5
            
            self.assertEqual(result, oracle)
            self.assertEqual(mock_connection.call_count, 1)




            









