import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock, patch
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.resultdao.result_dao_impl import ResultDAOImpl
from src.main.model.entity.result import Result

class TestResultDAOImpl(unittest.TestCase):
    patch_execute_action = "src.main.model.dao.resultdao.result_dao_impl.ResultDAOImpl.execute_action"
    patch_execute_select = "src.main.model.dao.resultdao.result_dao_impl.ResultDAOImpl.execute_select"

    """ Test __init__ """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = ResultDAOImpl(connection.connection, connection.cursor)
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)
        connection.close()

    """ Test create """

    def test_2_create_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            r_test = Result(0, "Risultato analisi statica", 2, 4)
            result = dao.create(r_test)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.CREATE, ("Risultato analisi statica", 2, 4), 1)
            connection.close()

    def test_3_create_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            r_test = Result(0, "Risultato analisi statica", 2, 4)
            try:
                dao.create(r_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.CREATE, ("Risultato analisi statica", 2, 4), 1)
                connection.close()

    """ Test read_by_id_analysis """

    def test_4_read_by_id_analysis_three_results(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [
                (2, "Risultato 1 analii statica", 10, 12),
                (4, "Risultato 2 analii statica", 10, 14),
                (6, "Risultato 3 analii statica", 10, 16)
            ]
            oracle = [
                Result(2, "Risultato 1 analii statica", 10, 12),
                Result(4, "Risultato 2 analii statica", 10, 14),
                Result(6, "Risultato 3 analii statica", 10, 16)
            ]
            result = dao.read_by_id_analysis(10)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID_ANALYSIS, (10,))

    def test_5_read_by_id_analysis_not_results(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            oracle = []
            result = dao.read_by_id_analysis(10)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID_ANALYSIS, (10,))

    def test_6_read_by_id_analysis_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_by_id_analysis(10)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_ID_ANALYSIS, (10,))
                connection.close()

    """ Test read_id_source_files_by_id_analysis """

    def test_7_read_id_source_files_by_id_analysis_three_results(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(10,), (20,), (30,)]
            oracle = [10, 20, 30]
            result = dao.read_id_source_files_by_id_analysis(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_SOURCE_FILES_BY_ID_ANALYSIS, (4,))

    def test_8_read_id_source_files_by_id_analysis_not_results(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            oracle = []
            result = dao.read_id_source_files_by_id_analysis(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_SOURCE_FILES_BY_ID_ANALYSIS, (4,))

    def test_9_read_id_source_files_by_id_analysis_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_id_source_files_by_id_analysis(4)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_SOURCE_FILES_BY_ID_ANALYSIS, (4,))
                connection.close()

    """ Test read_num_results_by_id_source_file """

    def test_10_read_num_results_by_id_source_file_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(10,)]
            oracle = 10
            result = dao.read_num_results_by_id_source_file(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_NUM_RESULTS_BY_ID_SOURCE_FILE, (4,))

    def test_11_read_num_results_by_id_source_file_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            oracle = 0
            result = dao.read_num_results_by_id_source_file(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_NUM_RESULTS_BY_ID_SOURCE_FILE, (4,))

    def test_12_read_num_results_by_id_source_file_result_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_num_results_by_id_source_file(4)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_NUM_RESULTS_BY_ID_SOURCE_FILE, (4,))
                connection.close()

    """ Test read_id_by_params """

    def test_13_read_id_by_params_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            r_test = Result(0, "Risultato analisi statica", 2, 4)
            mock_execute_select.return_value = [(10,)]
            oracle = 10
            result = dao.read_id_by_params(r_test)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, ("Risultato analisi statica", 2, 4))

    def test_14_read_id_by_params_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            r_test = Result(0, "Risultato analisi statica", 2, 4)
            mock_execute_select.return_value = []
            oracle = 0
            result = dao.read_id_by_params(r_test)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, ("Risultato analisi statica", 2, 4))

    def test_15_read_id_by_params_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDAOImpl(connection.connection, connection.cursor)
            r_test = Result(0, "Risultato analisi statica", 2, 4)
            mock_execute_select.return_value = None
            try:
                dao.read_id_by_params(r_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, ("Risultato analisi statica", 2, 4))
                connection.close()










