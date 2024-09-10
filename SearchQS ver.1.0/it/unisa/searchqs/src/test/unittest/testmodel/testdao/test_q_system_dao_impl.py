import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock, patch
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.qsystemdao.q_system_dao_impl import QSystemDAOImpl
from src.main.model.entity.q_system import QSystem

class TestQSystemDAOImpl(unittest.TestCase):
    patch_execute_action = "src.main.model.dao.qsystemdao.q_system_dao_impl.QSystemDAOImpl.execute_action"
    patch_execute_select = "src.main.model.dao.qsystemdao.q_system_dao_impl.QSystemDAOImpl.execute_select"

    """ Test __init__ """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = QSystemDAOImpl(connection.connection, connection.cursor)
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)
        connection.close()
        
    """ Test create """

    def test_2_create_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            qs_test = QSystem(0, "SistemaQuantistico.zip", "av_90@test.test")
            result = dao.create(qs_test)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.CREATE, ("SistemaQuantistico.zip", "av_90@test.test"), 1)
            connection.close()

    def test_3_create_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            qs_test = QSystem(0, "SistemaQuantistico.zip", "av_90@test.test")
            try:
                dao.create(qs_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.CREATE, ("SistemaQuantistico.zip", "av_90@test.test"), 1)
                connection.close()

    """ Test read_by_email_registered_user """

    def test_4_read_by_email_registered_user_results_success(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            names_qs = ["SistemaQuantistico1.zip", "SistemaQuantistico2.zip", "SistemaQuantistico3.zip"]
            email_ru = "test@test.test"
            mock_execute_select.return_value = [
                (1, names_qs[0], email_ru), 
                (2, names_qs[1], email_ru), 
                (3, names_qs[2], email_ru)
            ]
            result = dao.read_by_email_registered_user(email_ru)
            oracle = [
                QSystem(1, names_qs[0], email_ru), 
                QSystem(2, names_qs[1], email_ru), 
                QSystem(3, names_qs[2], email_ru)
            ]
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_EMAIL_REGISTERED_USER, (email_ru,))
            connection.close()

    def test_5_read_by_email_registered_user_not_result_success(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            email_ru = "test@test.test"
            mock_execute_select.return_value = []
            result = dao.read_by_email_registered_user(email_ru)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_EMAIL_REGISTERED_USER, (email_ru,))
            connection.close()

    def test_6_read_by_email_registered_user_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            email_ru = "test@test.test"
            mock_execute_select.return_value = None
            try:
                dao.read_by_email_registered_user(email_ru)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_EMAIL_REGISTERED_USER, (email_ru,))
                connection.close()

    """ Test read_by_name_and_email_registered_user """

    def test_7_read_by_name_and_email_registered_user_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            name_qs = "SistemaQuantistico.zip"
            email_ru = "test@test.test"
            mock_execute_select.return_value = [(2, name_qs, email_ru)]
            result = dao.read_by_name_and_email_registered_user(name_qs, email_ru)
            oracle = QSystem(2, name_qs, email_ru)
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_NAME_AND_EMAIL_REGISTERED_USER, 
                                                        (name_qs, email_ru))
            connection.close()

    def test_8_read_by_name_and_email_registered_user_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            name_qs = "SistemaQuantistico.zip"
            email_ru = "test@test.test"
            mock_execute_select.return_value = []
            result = dao.read_by_name_and_email_registered_user(name_qs, email_ru)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_NAME_AND_EMAIL_REGISTERED_USER, 
                                                        (name_qs, email_ru))
            connection.close()

    def test_9_read_by_name_and_email_registered_user_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            name_qs = "SistemaQuantistico.zip"
            email_ru = "test@test.test"
            mock_execute_select.return_value = None
            try:
                dao.read_by_name_and_email_registered_user(name_qs, email_ru)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_NAME_AND_EMAIL_REGISTERED_USER, 
                                                        (name_qs, email_ru))
                connection.close()

    """ Test read_id_by_email_registered_user """

    def test_10_read_id_q_systems_by_email_registered_user_results_success(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            email_ru = "test@test.test"
            mock_execute_select.return_value = [(1,), (2,), (3,)]
            result = dao.read_id_q_systems_by_email_registered_user(email_ru)
            oracle = [1, 2, 3]
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_Q_SYSTEMS_BY_EMAIL_REGISTERED_USER, (email_ru,))
            connection.close()

    def test_11_read_id_q_systems_by_email_registered_user_not_result_success(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            email_ru = "test@test.test"
            mock_execute_select.return_value = []
            result = dao.read_id_q_systems_by_email_registered_user(email_ru)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_Q_SYSTEMS_BY_EMAIL_REGISTERED_USER, (email_ru,))
            connection.close()

    def test_12_read_id_q_systems_by_email_registered_user_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            email_ru = "test@test.test"
            mock_execute_select.return_value = None
            try:
                dao.read_id_q_systems_by_email_registered_user(email_ru)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_Q_SYSTEMS_BY_EMAIL_REGISTERED_USER, (email_ru,))
                connection.close()

    """ Test read_id_by_attributes """

    def test_13_read_id_by_attributes_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            name_qs = "SistemaQuantistico.zip"
            email_ru = "mr_80@test.test"
            qs_test = QSystem(0, name_qs, email_ru)
            mock_execute_select.return_value = [(10,)]
            result = dao.read_id_by_attributes(qs_test)
            oracle = 10
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_ATTRIBUTES, (name_qs, email_ru))
            connection.close()

    def test_14_read_id_by_attributes_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            name_qs = "SistemaQuantistico.zip"
            email_ru = "mr_80@test.test"
            qs_test = QSystem(0, name_qs, email_ru)
            mock_execute_select.return_value = []
            result = dao.read_id_by_attributes(qs_test)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_ATTRIBUTES, (name_qs, email_ru))
            connection.close()
        
    def test_15_read_id_by_attributes_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            name_qs = "SistemaQuantistico.zip"
            email_ru = "mr_80@test.test"
            qs_test = QSystem(0, name_qs, email_ru)
            mock_execute_select.return_value = None
            try:
                dao.read_id_by_attributes(qs_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_BY_ATTRIBUTES, (name_qs, email_ru))
                connection.close()

    """ Test delete_by_id """

    def test_16_delete_by_id_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            result = dao.delete_by_id(10)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.DELETE_BY_ID, (10,), 1)
            connection.close()

    def test_17_delete_by_id_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = QSystemDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            try:
                dao.delete_by_id(10)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.DELETE_BY_ID, (10,), 1)
                connection.close()







