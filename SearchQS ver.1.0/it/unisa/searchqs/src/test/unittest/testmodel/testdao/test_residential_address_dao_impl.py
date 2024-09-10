import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock, patch
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.residentialaddressdao.residential_address_dao_impl import ResidentialAddressDAOImpl
from src.main.model.entity.residential_address import ResidentialAddress

class TestResidentialAddressDAOImpl(unittest.TestCase):
    patch_execute_action = "src.main.model.dao.residentialaddressdao.residential_address_dao_impl.ResidentialAddressDAOImpl.execute_action"
    patch_execute_select = "src.main.model.dao.residentialaddressdao.residential_address_dao_impl.ResidentialAddressDAOImpl.execute_select"

    """ Test __init__ """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)
        connection.close()

    """ Test create """

    def test_2_create_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            ra_test = ResidentialAddress(0, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            result = dao.create(ra_test)

            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.CREATE, 
                                                        ("Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086"), 1)
            connection.close()

    def test_3_create_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            ra_test = ResidentialAddress(0, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            try:
                dao.create(ra_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.CREATE, 
                                                        ("Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086"), 1)
                connection.close()

    """ Test read_by_id """

    def test_4_read_by_id_result_success(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(10, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")]
            oracle = ResidentialAddress(10, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            result = dao.read_by_id(10)
            connection.close()
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID, (10,))

    def test_5_read_by_id_not_result_success(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            oracle = []
            result = dao.read_by_id(10)
            connection.close()
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID, (10,))

    def test_6_read_by_id_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_by_id(10)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_ID, (10,))
                connection.close()

    """ Test read_id_by_params """

    def test_7_read_id_by_params_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(10,)]
            ra_test = ResidentialAddress(0, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            oracle = 10
            result = dao.read_id_by_params(ra_test)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, 
                                                        ("Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086"))

    def test_8_read_id_by_params_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            ra_test = ResidentialAddress(0, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            oracle = []
            result = dao.read_id_by_params(ra_test)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, 
                                                        ("Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086"))

    def test_9_read_id_by_params_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            ra_test = ResidentialAddress(0, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            try:
                dao.read_id_by_params(ra_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, 
                                                            ("Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086"))
                connection.close()

    """ Test delete_by_id """

    def test_10_delete_by_id_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            result = dao.delete_by_id(10)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.DELETE_BY_ID, (10,), 1)
            connection.close()
            
    def test_11_delete_by_id_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            try:
                dao.delete_by_id(10)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.DELETE_BY_ID, (10,), 1)
                connection.close()









