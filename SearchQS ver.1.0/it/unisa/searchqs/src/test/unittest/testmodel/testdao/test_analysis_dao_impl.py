import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock, patch
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.analysisdao.analysis_dao_impl import AnalysisDAOImpl
from src.main.model.entity.analysis import Analysis

class TestAnalysisDAOImpl(unittest.TestCase):
    PATCH_EXECUTE_ACTION = "src.main.model.dao.analysisdao.analysis_dao_impl.AnalysisDAOImpl.execute_action"
    PATCH_EXECUTE_SELECT = "src.main.model.dao.analysisdao.analysis_dao_impl.AnalysisDAOImpl.execute_select"

    """ Test __init__ """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = AnalysisDAOImpl(connection.connection, connection.cursor)
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)
        connection.close()
        
    """ Test create """

    def test_2_create_success(self):
        with patch(self.PATCH_EXECUTE_ACTION) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            a_test = Analysis(0, 'ibm_perth', 2, '2024-01-01', 4)
            result = dao.create(a_test)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.CREATE, ('ibm_perth', 2, '2024-01-01', 4), 1)
            connection.close()

    def test_3_create_failure(self):
        with patch(self.PATCH_EXECUTE_ACTION) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            a_test = Analysis(0, 'ibm_perth', 2, '2024-01-01', 4)
            try:
                dao.create(a_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.CREATE, ('ibm_perth', 2, '2024-01-01', 4), 1)
                connection.close()

    """ Test read_by_id_q_system_without_transpilation """

    def test_4_read_by_id_q_system_without_transpilation_results_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [
                (1, None, 2, '2023-01-02 01:02:03', 2),
                (2, None, 2, '2023-03-04 04:05:06', 2),
                (3, None, 2, '2023-05-06 07:08:09', 2)
            ]
            result = dao.read_by_id_q_system_without_transpilation(2)
            oracle = [
                Analysis(1, None, 2, '2023-01-02 01:02:03', 2),
                Analysis(2, None, 2, '2023-03-04 04:05:06', 2),
                Analysis(3, None, 2, '2023-05-06 07:08:09', 2)
            ]
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID_Q_SYSTEM_WITHOUT_TRANSPILATION, (2,))
            connection.close()

    def test_5_read_by_id_q_system_without_transpilation_not_results_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            result = dao.read_by_id_q_system_without_transpilation(2)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID_Q_SYSTEM_WITHOUT_TRANSPILATION, (2,))
            connection.close()

    def test_6_read_by_id_q_system_without_transpilation_failure(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_by_id_q_system_without_transpilation(2)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_ID_Q_SYSTEM_WITHOUT_TRANSPILATION, (2,))
                connection.close()

    """ Test read_by_name_transpilation_and_id_q_system """

    def test_7_read_by_name_transpilation_and_id_q_system_results_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [
                (1, "ibm_perth", 2, '2023-01-02 01:02:03', 2),
                (2, "ibm_perth", 2, '2023-03-04 04:05:06', 2),
                (3, "ibm_perth", 2, '2023-05-06 07:08:09', 2)
            ]
            result = dao.read_by_name_transpilation_and_id_q_system("ibm_perth", 2)
            oracle = [
                Analysis(1, "ibm_perth", 2, '2023-01-02 01:02:03', 2),
                Analysis(2, "ibm_perth", 2, '2023-03-04 04:05:06', 2),
                Analysis(3, "ibm_perth", 2, '2023-05-06 07:08:09', 2)
            ]
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_NAME_TRANSPILATION_AND_ID_Q_SYSTEM, ("ibm_perth", 2))
            connection.close()

    def test_8_read_by_name_transpilation_and_id_q_system_not_results_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            result = dao.read_by_name_transpilation_and_id_q_system("ibm_perth", 2)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_NAME_TRANSPILATION_AND_ID_Q_SYSTEM, ("ibm_perth", 2))
            connection.close()

    def test_9_read_by_name_transpilation_and_id_q_system_failure(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_by_name_transpilation_and_id_q_system("ibm_perth", 2)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_NAME_TRANSPILATION_AND_ID_Q_SYSTEM, ("ibm_perth", 2))
                connection.close()
    
    """ Test read_id_by_id_q_system """

    def test_10_read_id_analyses_by_id_q_system_result_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(1,), (2,), (3,)]
            result = dao.read_id_analyses_by_id_q_system(2)
            oracle = [1, 2, 3]
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_ANALYSES_BY_ID_Q_SYSTEM, (2,))
            connection.close()

    def test_11_read_id_analyses_by_id_q_system_not_results_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            result = dao.read_id_analyses_by_id_q_system(2)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_ANALYSES_BY_ID_Q_SYSTEM, (2,))
            connection.close()

    def test_12_read_id_analyses_by_id_q_system_failure(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_id_analyses_by_id_q_system(2)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_ANALYSES_BY_ID_Q_SYSTEM, (2,))
                connection.close()

    """ Test read_num_analyses_by_id_q_system """

    def test_13_read_num_analyses_by_id_q_system_result_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(4,)]
            result = dao.read_num_analyses_by_id_q_system(2)
            oracle = 4
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_NUM_ANALYSES_BY_ID_Q_SYSTEM, (2,))
            connection.close()

    def test_14_read_num_analyses_by_id_q_system_not_results_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            result = dao.read_num_analyses_by_id_q_system(2)
            oracle = 0
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_NUM_ANALYSES_BY_ID_Q_SYSTEM, (2,))
            connection.close()

    def test_15_read_num_analyses_by_id_q_system_failure(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_num_analyses_by_id_q_system(2)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_NUM_ANALYSES_BY_ID_Q_SYSTEM, (2,))
                connection.close()

    """ Test read_id_by_params """

    def test_16_read_id_by_params_result_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            a_test = Analysis(0, 'ibm_perth', 2, '2024-01-01', 4)
            mock_execute_select.return_value = [(10,)]
            result = dao.read_id_by_params(a_test)
            oracle = 10
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, ('ibm_perth', 2, '2024-01-01', 4))
            connection.close()

    def test_17_read_id_by_params_not_result_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            a_test = Analysis(0, 'ibm_perth', 2, '2024-01-01', 4)
            mock_execute_select.return_value = []
            result = dao.read_id_by_params(a_test)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, ('ibm_perth', 2, '2024-01-01', 4))
            connection.close()
        
    def test_18_read_id_by_params_failure(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            a_test = Analysis(0, 'ibm_perth', 2, '2024-01-01', 4)
            mock_execute_select.return_value = None
            try:
                dao.read_id_by_params(a_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS, ('ibm_perth', 2, '2024-01-01', 4))
                connection.close()

    """ Test read_id_by_params_with_name_transpilation_none """

    def test_19_read_id_by_params_with_name_transpilation_none_result_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            a_test = Analysis(0, None, 2, '2024-01-01', 4)
            mock_execute_select.return_value = [(10,)]
            result = dao.read_id_by_params_with_name_transpilation_none(a_test)
            oracle = 10
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE, (2, '2024-01-01', 4))
            connection.close()

    def test_20_read_id_by_params_with_name_transpilation_none_not_result_success(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            a_test = Analysis(0, None, 2, '2024-01-01', 4)
            mock_execute_select.return_value = []
            result = dao.read_id_by_params_with_name_transpilation_none(a_test)
            oracle = []
            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE, (2, '2024-01-01', 4))
            connection.close()
        
    def test_21_read_id_by_params_with_name_transpilation_none_failure(self):
        with patch(self.PATCH_EXECUTE_SELECT) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            a_test = Analysis(0, None, 2, '2024-01-01', 4)
            mock_execute_select.return_value = None
            try:
                dao.read_id_by_params_with_name_transpilation_none(a_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE, (2, '2024-01-01', 4))
                connection.close()

    """ Test delete_by_id """

    def test_22_delete_by_id_success(self):
        with patch(self.PATCH_EXECUTE_ACTION) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            result = dao.delete_by_id(10)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.DELETE_BY_ID, (10,), 1)
            connection.close()

    def test_23_delete_by_id_failure(self):
        with patch(self.PATCH_EXECUTE_ACTION) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            try:
                dao.delete_by_id(10)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.DELETE_BY_ID, (10,), 1)
                connection.close()
















