import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock, patch
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.sourcefiledao.source_file_dao_impl import SourceFileDAOImpl
from src.main.model.entity.source_file import SourceFile
import src.test.utils.utils as utils

class TestSourceFileDAOImpl(unittest.TestCase):
    patch_execute_action = "src.main.model.dao.sourcefiledao.source_file_dao_impl.SourceFileDAOImpl.execute_action"
    patch_execute_select = "src.main.model.dao.sourcefiledao.source_file_dao_impl.SourceFileDAOImpl.execute_select"

    """ Test __init__ """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = SourceFileDAOImpl(connection.connection, connection.cursor)
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)
        connection.close()

    """ Test create """

    def test_2_create_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
            mock_execute_action.return_value = True
            sf_test = SourceFile(0, file_path, "")
            sf_test.set_file_from_code(utils.code)
            result = dao.create(sf_test)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(
                    dao.CREATE, (sf_test.path, sf_test.file), 1)
            connection.close()

    def test_3_create_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
            mock_execute_action.side_effect = Exception
            sf_test = SourceFile(0, file_path, "")
            try:
                dao.create(sf_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(
                        dao.CREATE, (sf_test.path, sf_test.file), 1)
                connection.close()

    """ Test read_by_id """

    def test_4_read_by_id_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
            sf_test = SourceFile(4, file_path, "")
            sf_test.set_file_from_code(utils.code)
            mock_execute_select.return_value = [(sf_test.id, sf_test.path, sf_test.file)]
            oracle = sf_test
            result = dao.read_by_id(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID, (4,))

    def test_5_read_by_id_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            oracle = []
            result = dao.read_by_id(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID, (4,))

    def test_6_read_by_id_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_by_id(4)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_ID, (4,))
                connection.close()

    """ Test read_by_params """

    def test_7_read_by_param_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
            sf_test = SourceFile(4, file_path, "")
            sf_test.set_file_from_code(utils.code)
            mock_execute_select.return_value = [(sf_test.id, sf_test.path, sf_test.file)]
            oracle = sf_test
            sf_test.id = 0
            result = dao.read_by_params(sf_test)
            sf_test.id = 4
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_PARAMS, (sf_test.path, sf_test.file))
            
    def test_8_read_by_params_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
            mock_execute_select.return_value = []
            sf_test = SourceFile(4, file_path, "")
            sf_test.set_file_from_code(utils.code)
            oracle = []
            sf_test.id = 0
            result = dao.read_by_params(sf_test)
            sf_test.id = 4
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_PARAMS, (sf_test.path, sf_test.file))
            
    def test_9_read_by_params_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
            mock_execute_select.return_value = None
            sf_test = SourceFile(4, file_path, "")
            sf_test.set_file_from_code(utils.code)
            sf_test.id = 0
            try:
                dao.read_by_params(sf_test)
                sf_test.id = 4
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_PARAMS, (sf_test.path, sf_test.file))
                connection.close()

    """ Test delete_by_id """

    def test_10_delete_by_id_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
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
            dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            try:
                dao.delete_by_id(10)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.DELETE_BY_ID, (10,), 1)
                connection.close()











